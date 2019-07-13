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
    const ext_path = vscode.extensions.getExtension('nelloy.lua-wc3').extensionPath;
    var script_path = path.join(ext_path, 'src', 'script');
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
        output_channel.show();
    }
    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json  
    let disposable = vscode.commands.registerCommand('lua-wc3.Build', () => {
        var tmp = vscode.workspace.getConfiguration("lua-wc3").get("sourceFolder");
        var src_path = (tmp) ? String(tmp) : '';
        tmp = vscode.workspace.getConfiguration("lua-wc3").get("destinationFolder");
        var dst_path = (tmp) ? String(tmp) : '';
        tmp = vscode.workspace.rootPath;
        var work_path = (tmp) ? String(tmp) : '';
        src_path = path.join(work_path, src_path);
        dst_path = path.join(work_path, dst_path);
        var cmd = '';
        //if (process.platform === 'win32') {cmd = script_path + 'lua-wc3.exe';}
        //if (process.platform === 'linux') {cmd = 'python3 ' + script_path + 'lua-wc3.py';}
        cmd = 'python ' + path.join(script_path, 'lua-wc3.py');
        cmd += ' ' + src_path + ' ' + dst_path;
        var workerProcess = child_process.exec(cmd, build_callback);
    });
    context.subscriptions.push(disposable);
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map