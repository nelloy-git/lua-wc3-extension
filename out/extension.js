"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
const child_process = require('child_process');
const ext_path = vscode.extensions.getExtension('nelloy.lua-wc3').extensionPath;
const script_path = ext_path + '/src/script/build.py';
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
function activate(context) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "lua-wc3" is now active!');
    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json  
    let disposable = vscode.commands.registerCommand('lua-wc3.Build', () => {
        var workerProcess = child_process.exec('python3 ' + script_path, function (error, stdout, stderr) {
            if (error) {
                console.log(error.stack);
                console.log('Signal received: ' + error.stack);
            }
            console.log('stdout: ' + stdout);
            console.log('stderr: ' + stderr);
        });
    });
    context.subscriptions.push(disposable);
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map