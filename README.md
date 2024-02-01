# Big Data Variable Selector Tool
A tool to automate variable selection for research on large datasets. The provided example is on the variable dictionary of the UK Biobank Dataset. It utilises the GPT-4 API to include/exclude and categorise the 8000+ variables in the UK Biobank. The tool analyses 20-variable-segments at a time to minimise risk of hallucinations, and includes a concise justification for the inclusion or exclusion of each variable for manual review. The tool outputs into a JSON formatted and organised txt file. 

Example Output:
```
{
"Variable":"Sex", 
"Path":"Population characteristics > Baseline characteristics", 
"Decision":"Include", 
"Category":"Demographic", 
"Reason":"Sex is known to influence the risk factors and outcomes of cardiovascular disease."
},
{
"Variable":"Weight method", 
"Path":"Assessment centre > Physical measures > Anthropometry > Body size measures", 
"Decision":"Exclude", 
"Category":"N/A", 
"Reason":"The method used for weight measurement does not affect cardiovascular disease risks."
},
```
