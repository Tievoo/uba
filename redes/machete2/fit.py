import subprocess, re, os
CH='google-chrome'
src=open('machete.html',encoding='utf-8').read()
def pages(pdf):
    out=subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout
    return int(re.search(r'Pages:\s+(\d+)',out).group(1))
def render(fs,page,out):
    h=re.sub(r'/\*FS\*/.*?/\*END\*/',f'/*FS*/{fs:.3f}pt/*END*/',src)
    h=re.sub(r'/\*PAGE\*/.*?/\*END\*/',f'/*PAGE*/{page}/*END*/',h)
    open('_tmp.html','w',encoding='utf-8').write(h)
    subprocess.run([CH,'--headless=new','--disable-gpu','--no-pdf-header-footer',f'--print-to-pdf={os.path.abspath(out)}',os.path.abspath('_tmp.html')],capture_output=True)
    return pages(out)
for name,page in [('A4','210mm 297mm'),('oficio','216mm 340mm')]:
    lo,hi=4.0,11.0
    for _ in range(12):
        mid=(lo+hi)/2
        if render(mid,page,'_t.pdf')<=2: lo=mid
        else: hi=mid
    n=render(lo,page,f'machete2_redes_{name}.pdf'); print(name,round(lo,3),'pt',n,'pages')
os.remove('_tmp.html'); os.remove('_t.pdf')
