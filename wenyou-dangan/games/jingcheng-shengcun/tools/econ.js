// 用法：node tools/econ.js data/tables.json
// 粗算每旬净收入、作物和牲畜回本、街市买卖差价、铺子升级回本。假设见 03-economy.md。
const T = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
const HUNGER_DECAY = 16, STAMINA = 100, ACTIONS = T.TOTAL_ACTIONS;
const foodCostPerHunger = 4 / 16; // 面馆馒头 4文 / 饥饿+16，不占行动
const avg = ([a, b]) => (a + b) / 2;
console.log('== 打工：每旬最多做几次、毛收入、扣掉饭钱后的净收入 ==');
const rows = T.JOBS.map(j => {
  const n = Math.min(ACTIONS, Math.floor(STAMINA / j.c));
  const gross = n * avg(j.pay);
  const food = (n * j.h + HUNGER_DECAY) * foodCostPerHunger;
  return { id: j.id, n: j.n, req: JSON.stringify(j.req || {}), times: n, gross: Math.round(gross), net: Math.round(gross - food), perStamina: +(avg(j.pay) / j.c).toFixed(2) };
}).sort((a, b) => a.net - b.net);
for (const r of rows) console.log([r.n, r.req, r.times, r.gross, r.net, r.perStamina].join(' | '));
console.log('\n== 种田：每块地每旬净利（每旬浇水，成熟旬数=ceil(grow/2)，不计农耕加成）==');
const sell = T.SELL_PRICE;
for (const [k, s] of Object.entries(T.SEEDS)) {
  const xun = Math.ceil(s.grow / 2);
  const rev = avg(s.yld) * sell[s.crop];
  console.log([s.n, '成熟' + xun + '旬', '产出均值' + rev, '种子' + s.price, '每旬净' + ((rev - s.price) / xun).toFixed(1)].join(' | '));
}
console.log('\n== 养殖：每头每旬净利（饲料 5 文/份；喂了就产出）==');
for (const [k, a] of Object.entries(T.ANIMALS)) {
  const net = sell[a.prod] - a.feed * 5;
  console.log([a.n, '买价' + a.price, '产品' + a.prod + sell[a.prod], '饲料' + a.feed * 5, '每旬净' + net, '回本旬数' + (a.price / net).toFixed(1), '卖出价' + a.sell].join(' | '));
}
console.log('\n== 街市：买价 vs 卖价 ==');
for (const it of T.MARKET_ITEMS) if (sell[it.n] !== undefined) console.log(it.n, it.price, '->', sell[it.n]);
console.log('\n== 铺子升级回本（Lv→Lv+1 花 2000*Lv，每旬基础 +2000）==');
for (let lv = 1; lv < T.SHOP_MAX_LEVEL; lv++) console.log('Lv' + lv + '->' + (lv + 1), '花费', 2000 * lv, '回本约', lv, '旬');
