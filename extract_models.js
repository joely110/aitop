const fs = require('fs');
const content = fs.readFileSync('/Users/mac/.claude/projects/-Users-mac-Documents-workspace-aitop/71d09ad3-a7c6-48de-987b-c945d2fb60d7/tool-results/bke1h98wl.txt', 'utf8');

// Debug: let's see what the raw data looks like around entry 10
const entries = content.split('modelName\\":\\"');
console.log('Total entries:', entries.length);

// Print entries 9-12 to see where the data changes
for (let i = 9; i <= 12 && i < entries.length; i++) {
  console.log(`\n--- Entry ${i} ---`);
  console.log(entries[i].substring(0, 300));
}

// Also check the total count of modelName occurrences in the original
const allMatches = content.match(/modelName/g);
console.log('\nTotal modelName occurrences:', allMatches ? allMatches.length : 0);