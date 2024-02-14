Set wshShell =wscript.CreateObject("WScript.Shell")
do
wscript.sleep 100
for i = 65 to 90
if wshshell.AppActivate("Notepad") then
wshshell.SendKeys chr(i)
end if
next
loop
