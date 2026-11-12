#!/usr/bin/python3
"""Cases for fm-dispatch-gate.py (27). Self-contained fixture; run: python3 test_fm_dispatch_gate.py"""
import json, subprocess, sys
import os, tempfile, shutil
G=os.path.join(os.path.dirname(os.path.abspath(__file__)),"fm-dispatch-gate.py")
FIXTURE={"rules":[
 {"when":"frontier research","use":[{"harness":"claude","model":"fable","effort":"xhigh"},{"harness":"codex","model":"gpt-6-astra","effort":"xhigh"},{"harness":"agy","model":"gemini-4-carbon-high","effort":"high"}]},
 {"when":"review","use":[{"harness":"codex","model":"gpt-6.1-sol","effort":"xhigh"},{"harness":"claude","model":"opus","effort":"xhigh"}]},
 {"when":"read-only","use":[{"harness":"agy","model":"gemini-4-argon-high","effort":"high"},{"harness":"codex","model":"gpt-6.1-sol","effort":"high"},{"harness":"claude","model":"opus","effort":"high"}]},
 {"when":"mechanical","use":[{"harness":"codex","model":"gpt-6-luna","effort":"medium"},{"harness":"agy","model":"gemini-3.8-flash-medium","effort":"medium"}]}],
 "default":[{"harness":"claude","model":"opus","effort":"medium"},{"harness":"codex","model":"gpt-6.1-sol","effort":"medium"}]}
HOME=tempfile.mkdtemp()
os.makedirs(HOME+"/config"); os.makedirs(HOME+"/state")
json.dump(FIXTURE,open(HOME+"/config/crew-dispatch.json","w"))
open(HOME+"/config/ship-harnesses","w").write("# test fixture\nclaude\nagy\n")
open(HOME+"/state/cx-scout.meta","w").write("harness=codex\nkind=scout\n")
open(HOME+"/state/cl-scout.meta","w").write("harness=claude\nkind=scout\n")
S="bin/fm-spawn.sh t1 projects/woe "
SH=S+"--mode no-mistakes --yolo off "
cases=[
 ("ship claude no model (today's bug)", SH+"--harness claude --effort medium", 2),
 ("ship claude opus medium (default)", SH+"--harness claude --model opus --effort medium", 0),
 ("ship codex sol medium", SH+"--harness codex --model gpt-6.1-sol --effort medium", 2),
 ("ship codex + override", SH+"--harness codex --model gpt-6.1-sol --effort medium --dispatch-override 'captain said'", 2),
 ("scout codex sol high", S+"--scout --harness codex --model gpt-6.1-sol --effort high", 0),
 ("scout codex sol low (no profile)", S+"--scout --harness codex --model gpt-6.1-sol --effort low", 2),
 ("scout claude override", S+"--scout --harness claude --dispatch-override \"captain asked for Fable\"", 0),
 ("scout empty override", S+"--scout --harness claude --dispatch-override ''", 2),
 ("grep mention", "grep -n crew bin/fm-spawn.sh", 0),
 ("sed mention", "sed -n 1,40p ~/firstmate/bin/fm-spawn.sh | head", 0),
 ("chained ok", "cd ~/firstmate && "+S+"--scout --harness agy --model gemini-4-argon-high --effort high", 0),
 ("chained bad", "cd ~/firstmate && "+S+"--scout --harness claude", 2),
 ("bash -c bad", "bash -c '"+S+"--scout --harness claude'", 2),
 ("relaunch", S+"--relaunch --harness claude", 0),
 ("secondmate", "bin/fm-spawn.sh mate1 --harness claude --secondmate", 0),
 ("promote codex scout", "bin/fm-promote.sh cx-scout --mode direct-PR --yolo off", 2),
 ("promote claude scout", "bin/fm-promote.sh cl-scout --mode direct-PR --yolo off", 0),
 ("batch agy scouts", "bin/fm-spawn.sh a=projects/x b=projects/y --scout --harness agy --model gemini-4-argon-high --effort high", 0),
 ("= form codex luna scout", S+"--scout --harness=codex --model=gpt-6-luna --effort=medium", 0),
 ("assignment prefix bad", "FM_BACKEND=herdr "+S+"--scout --harness claude --effort high", 2),
 ("help", "bin/fm-spawn.sh --help", 0),
 ("raw launch scout", S+"--scout 'codex --yolo'", 2),
 ("positional harness ok", S+"--scout claude --model opus --effort high", 0),
 ("agy ship flash medium", SH+"--harness agy --model gemini-3.8-flash-medium --effort medium", 0),
 ("unrelated", "git status && ls state", 0),
 ("multiline second line bad", "echo hi\n"+S+"--scout --harness codex", 2),
]
bad=0
for name,cmd,want in cases:
    p=subprocess.run([sys.executable,G],input=json.dumps({"tool_name":"Bash","tool_input":{"command":cmd},"cwd":HOME}),capture_output=True,text=True,env={"CLAUDE_PROJECT_DIR":HOME,"PATH":"/usr/bin:/bin"})
    ok = p.returncode==want
    bad += not ok
    print(("PASS" if ok else "FAIL"), p.returncode, name, ("| "+p.stderr.strip()[:160]) if p.stderr else "")
p=subprocess.run([sys.executable,G],input=json.dumps({"tool_name":"Read","tool_input":{"file_path":"x"}}),capture_output=True,text=True)
print("PASS" if p.returncode==0 else "FAIL", "non-Bash tool")
print("failures:",bad)
shutil.rmtree(HOME)
sys.exit(1 if bad else 0)
