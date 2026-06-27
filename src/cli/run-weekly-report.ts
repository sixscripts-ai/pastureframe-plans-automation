import { weeklyReportWorkflow } from '../workflows/weekly_report.js';
const r = await weeklyReportWorkflow();
console.log(JSON.stringify(r, null, 2));
