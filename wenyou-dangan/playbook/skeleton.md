---
type: playbook
status: active
updated: 2026-10-29
sources: [games/jingcheng-shengcun/01-tech.md]
---

# 单 HTML 文游技术骨架

从「京城生存挑战」提炼，再按设计理念补了两样：目标栏和存档迁移。整套只要原生 JS，不用框架，也不用构建；一个 HTML 文件，手机点开就能玩。下面的代码是示意，写新作时照着搭，不要原样粘贴。

## 1. 总体结构

```
<head>  viewport + 一段 CSS（颜色变量放在 :root）
<body>
  #start   开场页：标题、开局文案、取名、开始按钮（同时启动 BGM）
  #phone   游戏主体（max-width: 430px）
    .top   顶栏：名字 · 回合 · 钱 · 住处 · 当前目标
    .mini  三条状态（健康 / 体力 / 饥饿）
    main   各页签的 .view（家 / 打工 / 街道 / 家产 / 换装 / 情缘 / 属性）
    nav    底部导航 + 「下一回合」按钮
  #mask > #sheet   唯一的弹窗
<script>  工具 → 数据表 → 状态 → 渲染 → 行动 → 结算 → 弹窗 / 事件队列 → 存档 → 绑定
```

## 2. 数据表驱动：加内容 = 加一行

```js
const JOBS = [
  { id:'sweep', n:'扫大街',   cost:13, hunger:6, pay:[14,26],  req:null },
  { id:'paint', n:'画坊描样', cost:16, hunger:7, pay:[96,164], req:{painting:15}, train:{painting:2} },
];
const HOUSING = { '破庙':{hp:-7, rent:0, price:0, unlock:[]}, '小院子':{hp:3, rent:0, price:4000, unlock:['farm']} };
```

- 数值表的唯一来源放在档案的 `data/*.json` 里；代码中的常量照它生成或照它抄。
- 门槛统一写成 `req:{属性:值}`，再配一个 `checkReq(req)` 和一个 `reqDesc(req)`：前者判断够不够，后者生成「需要 智慧≥30」这类锁定提示。

## 3. 状态：一个对象装下全部

```js
const DEFAULTS = { v:1, name:'', turn:1, actions:0, money:50, health:80, stamina:100, hunger:60,
  stats:{ beauty:20, wisdom:20 }, skills:{}, house:'破庙', flags:{}, npcs:{}, logs:[] };
let S = null;
function newGame(name){ S = structuredClone(DEFAULTS); S.name = name; renderAll(); }
```

存档就是 `JSON.stringify(S)`。原作每加一个字段，读档时就要多写一行 `if(x===undefined)`（`page.html:3763` 那一长串）。改成按默认值递归补齐：

```js
const isObj = o => o && typeof o === 'object' && !Array.isArray(o);
function migrate(data, def = DEFAULTS){
  for (const k in def){
    if (data[k] === undefined) data[k] = structuredClone(def[k]);
    else if (isObj(def[k]) && isObj(data[k])) migrate(data[k], def[k]);
  }
  return data;   // 每个 NPC 的字段另用 NPC_DEFAULT 逐个 migrate
}
```

## 4. 行动预算

```js
const MAX_ACTIONS = 8;
function spend(cost){
  if (S.actions >= MAX_ACTIONS) { toast('本回合行动用完了'); return false; }
  if (S.stamina < cost)         { toast('体力不够'); return false; }
  S.actions++; S.stamina -= cost;
  if (S.actions === MAX_ACTIONS / 2) S.night = true;   // 原作：第 4 次行动后入夜
  return true;
}
```

哪些操作占行动要想清楚。原作里买卖、吃饭、送礼都不占行动，这正是零成本刷名气、刷好感的漏洞来源（见 [economy.md](economy.md)）。

## 5. 渲染与交互

- 每个页签写一个 `renderXxx()`，返回 innerHTML；`renderAll()` 重画顶栏和当前页签。这个规模全量重画没问题。
- 交互统一挂在 `main` 上做事件委托，用一张动作注册表分发，别写长长的 if 链（原作 `page.html:3876`）：

```js
const ACTS = { job: id => doJob(id), place: id => doPlace(id), visit: id => visitNpc(id) };
$('main').addEventListener('click', e => {
  const el = e.target.closest('[data-act]');
  if (el && !el.disabled) ACTS[el.dataset.act]?.(el.dataset.arg);
});
// <div class="card" data-act="job" data-arg="sweep">…</div>
```

## 6. 唯一的弹窗 showSheet

商店、选择、剧情、确认，全部用它（原作 `page.html:3491`）。每个选项写成 `{t:标题, s:后果小字, fn:回调}`，后果直接写在 `s` 里，比如「好感+20 · 健康-5」。

```js
let sheetCancel = null;
function showSheet(title, opts, onCancel){
  $('sheet').innerHTML = `<div class="st">${title}</div>`;
  const wrap = document.createElement('div');
  for (const o of opts){
    const b = document.createElement('button');
    b.innerHTML = o.s ? `${o.t}<small>${o.s}</small>` : o.t;
    b.onclick = () => { closeSheet(); o.fn?.(); };
    wrap.appendChild(b);
  }
  $('sheet').appendChild(wrap);
  $('mask').classList.add('show');
  sheetCancel = onCancel || null;   // 点遮罩关闭时调用，例如「没回答 = 拒绝」
}
```

## 7. 事件队列

回合结算时，所有触发的剧情都先入队，再一个接一个弹出来。原作用 `setInterval` 每 100ms 检查弹窗关没关（`page.html:2937`），改成回调链更稳：

```js
const queue = []; let showing = false;
const pushEvent = (text, opts, onCancel) => queue.push({ text, opts, onCancel });
function runQueue(){
  if (showing || !queue.length) return;
  showing = true;
  const ev = queue.shift();
  const done = () => { showing = false; save(); renderAll(); runQueue(); };
  const opts = (ev.opts?.length ? ev.opts : [{ t:'知道了' }])
    .map(o => ({ ...o, fn: () => { o.fn?.(); done(); } }));
  showSheet(ev.text, opts, () => { ev.onCancel?.(); done(); });
}
```

规矩：事件选项里不要直接再开弹窗，要开就 `pushEvent`，让它排进队列。

## 8. 回合结算流水线

原作的 `nextXun`（`page.html:3246`）把十几步写在一个函数里。改成有序的步骤数组：顺序一目了然，加一步只多一行。

```js
const SETTLE = [
  upkeep,        // 饥饿下降、住所扣血或回血、生病
  pregnancy,     // 孕期推进、生产
  bills,         // 房租、学费、人情
  passiveIncome, // 铺子、存款利息、配偶贴补
  growth,        // 作物、牲畜、子女年龄
  pressure,      // 原生家庭、随机夜间事件
  stories,       // 主线目标、角色好感剧情、修罗场
  deathCheck,
];
function nextTurn(){
  S.turn++; S.actions = 0; S.night = false;
  SETTLE.forEach(step => step());
  S.stamina = S.staminaMax;
  save(); renderAll(); runQueue();
}
```

## 9. 目标栏（原作没有，按理念 3 补上）

```js
const QUESTS = [
  { id:'roof',  text:'攒 800 文，搬出破庙',          done: () => S.house !== '破庙' },
  { id:'craft', text:'把任一技能练到 15，换份体面活', done: () => Object.values(S.skills).some(v => v >= 15) },
  { id:'sever', text:'攒够四两银子，和那家人了断',    done: () => S.flags.severed },
];
const currentQuest = () => QUESTS.find(q => !q.done());
// 顶栏：🎯 ${currentQuest()?.text ?? '自由时光'}；完成时 pushEvent 一段剧情，再给奖励
```

主线节拍怎么排，见 [narrative.md](narrative.md)。

## 10. 存档

- 每次行动后自动存一份，另外留 6 个手动槽位。key 带上游戏名和版本前缀，比如 `jcss8_slot1`。
- **导出 / 导入为文本**：微信内置浏览器可能清掉 localStorage，玩家换手机也要能迁移。原作超过 1 万字就分批复制，并提示「粘到微信文件传输助手」（`page.html:3562`）。这个做法要保留。
- 自动存档里的日志截断到最近 30 条，控制体积。

## 11. 手机适配

- `<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">`
- 容器高度用 `100dvh`。原作用 `100vh`，iOS 地址栏会把底部导航挤出屏幕。底部导航加 `padding-bottom: env(safe-area-inset-bottom)`。
- `touch-action: manipulation`，再屏蔽双击缩放（原作 `page.html:258`）。
- 用 `busy` 标记防止连点；连点会重复结算的按钮（如睡觉）再单独做 300ms 防抖。
- 古风感几乎全靠配色变量（深棕底、金字）和楷体字体栈：`"KaiTi","STKaiti","Songti SC",serif`。

## 12. 资源

- BGM 只能在用户点击之后 `play()`（浏览器禁止自动播放），所以放在开始按钮的回调里，并提供开关。建议再加一条：`visibilitychange` 时暂停。
- 不要用免费图床：链接一失效，游戏就没图了。托管方式见 [assets.md](assets.md)。

## 13. 可测试的模型段

把所有改状态的逻辑（数据表、行动、结算、剧情、结局）放进一段，用注释标出边界，这一段里不碰 DOM：

```js
/*MODEL-START*/
let R = Math.random; function setRng(f){ R = f; }    // 测试时换成带种子的随机数
const HOOKS = { unlock(){}, checkpoint(){}, sfx(){} }; // 界面层再覆盖这些钩子
const EVQ = [];                                        // 剧情事件只入队，由界面层弹出
function gather(S){ … } function endDay(S){ … }
/*MODEL-END*/
```

node 里截出这一段，用 `vm.runInNewContext(model + ';({gather, endDay, …})')` 就能跑机器人对局（[economy.md §7](economy.md)）。事件选项的 `fn` 只改 S；要接着弹下一个，就 `EVQ.unshift(...)`。

## 14. 两种发布形态

- **Artifact（试玩链接）**：源文件不写 `<!doctype>`、`<html>`、`<head>`、`<body>`，发布时平台会自动包一层；文件开头直接写 `<title>`、`<style>`。本地存储的读写都包上 try/catch；没有 `alert` / `confirm`，确认都做成弹窗。
- **独立版（发给玩家）**：用档案里的 `tools/build.sh` 补上 doctype、head、viewport，生成可以双击打开的文件。Google Fonts 在国内可能加载不到，字体栈要以系统楷体、宋体兜底。
- **公开链接（GitHub Pages）**：独立版放进 `Tonkmy/bin` 仓库的 `<slug>/index.html`，再在根目录 `index.html` 的目录里加一条；仓库 README 里写了步骤。地址是 `https://tonkmy.github.io/bin/<slug>/`。

## 15. 上线前必查

- **外部字体用脚本异步加载**，不要用 `<link rel="stylesheet">` 直接写在 head 里。国内连不上 Google Fonts 时，阻塞式加载会让页面白屏很久。Canvas 上用到的字体，要监听 `document.fonts` 的 `loadingdone` 事件，加载完再重画一遍。
- **存档键名加游戏前缀**：`tonkmy.github.io` 下所有游戏共用一份 localStorage，键名重复会互相覆盖存档。
