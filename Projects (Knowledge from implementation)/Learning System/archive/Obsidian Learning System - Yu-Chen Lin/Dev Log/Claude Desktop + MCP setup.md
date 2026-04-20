%%I guess in the beginning of a task I can have a table of contents to kind of understand what is in this task %%
Tasks 
- [ ] Install Local REST API plugin
- [ ] Install MCP-tools plugin
	- [ ] [[Learn what the recommended plugins (Templator & Smart Connector) are]]
	- [ ] Install the recommended plugins  %%I didn't %%

%% Tasks that don't branch into further tasks can be  represented as text under titles or headers instead of links to task files or actually dev logs like below
um but these tasks don't actually need a header them selves right ? becuase I want to demonstrate the thought process or incidents or  problems and solutions I have met
%%

Happening : 
1. Not seeing hammer after installing the REST API and MCP-tools plugin - meaning that Claude isnot connected to the installed MCP server. 
	-> It was because I didn't restart Claude - After restart, Claude asked permissions to access the mcp-server folder in the plugin. 
	-> Still didn't see hammer after restart %% Don't know if I should let this be 2. %%
	-> Looked at log files in the Claude MCPs
	-> Claude says that the connection is working 
	-> Had 404 error for `GET /vault/Prompts/` -> Thought that connection is not working
	-> Claude said to create a Prompts folder or install Templater plugin, he said issue was gue to Templater not being installed. 
	-> Installed -> same error
	-> Pasted several screenshots to Claude 
	-> Confirmed the MCP server is running, just the hammer is not working
2. Why do we still have 404 problem
	-> It's just that we don't have the Prompts folder so we get 404 when trying to call it, like web.
3. Came up with the framework and instructions for Claude to create files to manage "Learning System", like the goal.md files, and dev logs starting with dates.
4. Prompted Claude to access Obsidian and take action
	-> Claude fails to perform "list_vault"
	-> tested Rest API connection by using url 
	-> says something with authenticated : false -> thought it was authentication problem 
	-> Modified config file (added / at the front of path)
	-> same error
	-> changed authentication key
	-> same error
	-> looked at log file asked AI 
	-> same error
	-> reinstalled restapi and MCP plugin
	-> same error 
	-> Ran a lot of tests trying to see the problem 
		```
		```2026-03-28T19:36:12.265Z [obsidian-mcp-tools] [info] Message from server: {"jsonrpc":"2.0","id":8,"error":{"code":-32603,"message":"MCP error -32603: GET /vault/ 404: {\n \"message\": \"Not Found\",\n \"errorCode\": 40400\n}"}} { metadata: undefined } 2026-03-28T19:38:00.064Z [obsidian-mcp-tools] [info] Message from client: {"method":"tools/call","params":{"name":"list_vault_files","arguments":{}},"jsonrpc":"2.0","id":9} { metadata: undefined } 2026-03-28T19:38:00.067Z [DEBUG] "Handling request" { "request": { "method": "tools/call", "params": { "name": "list_vault_files", "arguments": {} } } } ```
	-> I questioned Claude if it could do other stuff besides list vault
	-> able to create, delete files in obsidian
	-> just list_vault_files not working
	
	-> asked Codex to debug for me
	-> Codex went through source code and pinpointed the lines in main.js saying that it only lists directories that contain files somwhere underneath it. At that time, I only had folders (a structure) wanting Claude to fill in for me. 
	-> Problem Solved
1. Claude generated the tests but I am not satisfied
	-> Come up with a sample version I wrote my self for further optimization  %% How do I let this link to my Obsidian Learning System%%
2. Discuss how to design the project management process better (using Learning System as an example)
	->
	
