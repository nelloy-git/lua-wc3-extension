"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
const child_process = require("child_process");
const path = require("path");
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
function activate(context) {
    var output_channel = vscode.window.createOutputChannel('lua-wc3');
    console.log('Init done');
    function build_callback(error, stdout, stderr) {
        output_channel.clear();
        if (error) {
            output_channel.append('Error: ' + error.code);
            output_channel.append('Signal received: ' + error.stack);
        }
        if (stdout !== '') {
            output_channel.append('Compiletime output:\n' + stdout);
        }
        if (stderr !== '') {
            output_channel.append('Error:\n' + stderr);
        }
        output_channel.append('\nDone');
        output_channel.show();
    }
    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json  
    let disposable = vscode.commands.registerCommand('lua-wc3.Build', () => {
        var src_path = getStringFromConf("sourceFolder");
        var dst_path = getStringFromConf("destinationFolder");
        var exe_path = getStringFromConf("exePath");
        var tmp = vscode.workspace.rootPath;
        var work_path = (tmp) ? String(tmp) : '';
        src_path = path.join(work_path, src_path);
        dst_path = path.join(work_path, dst_path);
        var cmd = '';
        if (exe_path.endsWith('.exe')) {
            cmd = exe_path;
        }
        if (process.platform === 'win32' && exe_path.endsWith('.py')) {
            cmd = 'python ' + exe_path;
        }
        if (process.platform === 'linux' && exe_path.endsWith('.py')) {
            cmd = 'python3 ' + exe_path;
        }
        cmd += ' ' + src_path + ' ' + dst_path;
        var workerProcess = child_process.exec(cmd, build_callback);
    });
    context.subscriptions.push(disposable);
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
function getStringFromConf(name) {
    var tmp = vscode.workspace.getConfiguration("lua-wc3").get(name);
    return tmp ? String(tmp) : '';
}
//# sourceMappingURL=extension.js.map