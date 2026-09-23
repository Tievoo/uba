import subprocess, fitz, re, sys, os
CH=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
src=open('machete.html',encoding='utf-8').read()
def render(fs,page,out):
    h=re.sub(r'/\*FS\*/.*?/\*END\*/',f'/*FS*/{fs:.3f}pt/*END*/',src)
    h=re.sub(r'/\*PAGE\*/.*?/\*END\*/',f'/*PAGE*/{page}/*END*/',h)
    open('_tmp.html','w',encoding='utf-8').write(h)
    subprocess.run([CH,'--headless=new','--disable-gpu','--no-pdf-header-footer',f'--print-to-pdf={os.path.abspath(out)}',os.path.abspath('_tmp.html')],capture_output=True)
    return len(fitz.open(out))
for name,page in [('A4','210mm 297mm'),('Oficio','216mm 340mm')]:
    lo,hi=4.0,11.0
    for _ in range(12):
        mid=(lo+hi)/2
        n=render(mid,page,'_t.pdf')
        if n<=2: lo=mid
        else: hi=mid
    n=render(lo,page,f'Machete_Redes_{name}.pdf'); print(name,round(lo,3),'pt',n,'pages')
os.remove('_tmp.html'); os.remove('_t.pdf')
