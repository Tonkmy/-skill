// 用法：node tools/extract.js <page.html 本地路径> > data/tables.json
// 只执行源码里的数据常量段（HOUSING 到 SHOP_MAX_LEVEL，外加 FOODS），NPC 的文案字段去掉（仓库公开）。
const fs = require('fs'), vm = require('vm');
const src = fs.readFileSync(process.argv[2], 'utf8');
const js = src.slice(src.indexOf('<script>') + 8, src.indexOf('</script>'));
const start = js.indexOf('const HOUSING=');
const end = js.indexOf('let S=null');
const foodsStart = js.indexOf('const FOODS=');
const foodsEnd = js.indexOf('function showEat');
const code = js.slice(start, end) + '\n' + js.slice(foodsStart, foodsEnd) +
  '\n;({HOUSING,HOUSE_ORDER,SKILL_DEFS,CLOTHES,JOBS,DISHES,MARKET_ITEMS,SELL_PRICE,SEEDS,ANIMALS,SHOP_TYPES,CHEAT_CHANCE,NPC_DEFS,SPOUSE_INCOME,BOOKS,SEASONS,SCHOOL_FEE,FAME_MAX,SAVE_SLOTS,MEET_CHANCE,NIGHT_ACTION_LIMIT,TOTAL_ACTIONS,WEDDING_COST,SHOP_MAX_LEVEL,FOODS})';
const T = vm.runInNewContext(code, {});
// Strip narrative prose from NPCs (public repo): keep metadata only.
const npcs = {};
for (const [k, d] of Object.entries(T.NPC_DEFS)) {
  npcs[k] = { name: d.name, age: d.age, sex: d.sex, title: d.title, type: d.type, loyalty: d.loyalty, meetAt: d.at, minXun: d.minXun };
}
T.NPC_DEFS = npcs;
process.stdout.write(JSON.stringify(T, null, 1));
