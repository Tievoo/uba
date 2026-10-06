# Hoja del parcial — tres versiones

Cada lado tiene 32 renglones a dos columnas: la línea N de cada columna va en el renglón N.

## Versión A — Plantillas
### Frente, columna izquierda
```text
# SEMÁFOROS · asumo débiles salvo que diga
señal   s=S(0)    A: x; s.rel()        B: s.acq(); y
rendez  a,b=S(0)  A: a.rel(); b.acq()  B: b.rel(); a.acq()
mutex m=S(1) · multiplex s=S(K) · alternancia pA=S(1) pB=S(0)
# LIGHTSWITCH (room, m, c)
entrar: m.acq; c++; if(c==1) room.acq; m.rel
salir:  m.acq; c--; if(c==0) room.rel; m.rel
prior. lectores: lector = LS(escribir) · escritor escribir.acq/rel
# SIN INANICIÓN: mol = S(1, true)
lector: mol.acq; mol.rel; LS.entrar ... (de pasada)
escritor: mol.acq; escribir.acq; mol.rel; E; escribir.rel
# PRIOR. ESCRITORES: leer, escribir, mutexL, mutexE, mutexP
lector: mutexP.acq; leer.acq; LS_L.entrar(escribir);
   leer.rel; mutexP.rel; LEER; LS_L.salir(escribir)
escritor: LS_E.entrar(leer); escribir.acq; E; escribir.rel;
   LS_E.salir(leer)      (mutexP: 1 solo lector compite en leer)
# PUENTE: mol.acq; LS[dir].entrar(res); mol.rel
cruzar (máx K: lugares.acq/rel alrededor); LS[dir].salir(res)
# BARRERA reutilizable
m.acq; c++; if(c==n) t1.rel ×n; m.rel; t1.acq
m.acq; c--; if(c==0) t2.rel ×n; m.rel; t2.acq
# PROD-CONS: nF=S(N) nE=S(0) mP mC
P: nF.acq; mP{ buf[in]=d; in++ }; nE.rel
C: nE.acq; mC{ d=buf[out]; out++ }; nF.rel
k unidades: mK.acq; k× u.acq; mK.rel ... k× u.rel (sin mK)
# PASO DE TESTIGO (FIFO sin fuertes)
entrar: m.acq; s=S(0); p=fila.vacía; fila.add(s); m.rel;
   if(p) s.rel; s.acq
salir: m.acq; fila.popFirst; sig=fila.peek; m.rel; if(sig) sig.rel
# BARBERO: m{ if lleno: me voy; else gente++ }
cli: sol.rel; listo.acq; corte; term.acq; m{gente--}; ret.rel
barb: sol.acq; listo.rel; corte; term.rel; ret.acq
```
### Frente, columna derecha
```text
# MONITORES · Mesa (E = W < S), sin spurious
esquema: while(!puedo) wait(c); cambio estado; signal/All(c')
sem→mon  V: x++; signal(cx)     P: while(x==0) wait(cx); x--
thread{ loop{ m.empezar(); ACCIÓN LARGA; m.terminar(); } }
# BARRERA con fase
esperar(){ miF=fase; c++;
   if(c==n){ c=0; fase++; signalAll(cv) }
   else while(fase==miF) wait(cv) }
# TICKETS (orden de llegada)
miT=prox++; while(miT!=turno || !puedo) wait(c)
...; turno++; signalAll(c)
# LIBERAR DE A N (Atrapador)
esperar: miT=prox++; signalAll(pLib); while(miT>=lib) wait(at)
liberar(N): while(prox-lib<N) wait(pLib); lib+=N; signalAll(at)
# RENDEZVOUS (barbero)
cli: esp++; signal(hayCli); while(llam==0) wait(cL); llam--
     while(term==0) wait(cT); term--
empezar: while(esp==0) wait(hayCli); esp--; llam++; signal(cL)
terminar: term++; signal(cT)
# SALA / RONDAS
asistir: while(enCurso||lleno) wait(ent); gente++;
   miCh=term; while(term==miCh) wait(fin)
cerrar: enCurso=F; gente=0; term++; signalAll(fin); signalAll(ent)
secuenc.: while(t!=n) wait(c[n]); f(); t=(n+1)%3; signal(c[t])
# MÁS PATRONES
pizzas: while(g==0 && ch<2) wait; if(g>0) g-- else ch-=2
no 2 seguidas: while(ult==yo && !fin) wait; ult=yo; ...; signalAll
bote: bool subiendo + orilla; la autorización se gasta al partir
recursos k: while(cant<k) wait; tomar k · liberar: signalAll
no perjudicar pedidos grandes: tickets, solo el primero toma
# HOARE: signal cede ya ⇒ while → if
(si solo se señala con la cond cierta; signalAll ⇒ sigue while)
```
### Dorso, columna izquierda
```text
# EJ 1 · MUTEX · sin DEADLOCK/livelock · sin INANICIÓN (=GdE)
SC termina; SNC puede no terminar; inanición = traza ∞ FAIR
x++  ≡  tmp=x; x=tmp+1
I   while(flag); flag=T; SC; flag=F            → rompe MUTEX
II  flag[i]=T; while(flag[o]); SC; flag[i]=F   → DEADLOCK
III while(turno!=i); SC; turno=o               → INANICIÓN
# DEKKER
flag[i]=T;
while(flag[o]){ if(turno==o){ flag[i]=F; while(turno==o); flag[i]=T } }
SC; turno=o; flag[i]=F
# PETERSON (2)
flag[i]=T; turno=o; while(flag[o] && turno==o); SC; flag[i]=F
mutex: el último en escribir turno espera · sin inanición
# BAKERY (N)
eligiendo[i]=T; num[i]=1+max(num); eligiendo[i]=F
∀j: while(eligiendo[j]); while(num[j]!=0 && (num[j],j)<(num[i],i))
SC; num[i]=0        (sin desempate por id → DEADLOCK)
ticket que se decrementa al salir → tickets repetidos → MUTEX
turno/proximo sin reset al salir el último → MUTEX (si reentran)
elegir siempre el menor id → INANICIÓN
traza:  | T1 | T2 | estado (PC, vars locales) |
probar "vale": invariante o absurdo ("el último en entrar vio...")
# (c) MODELO DE MEMORIA
todo lo anterior supone SC (interleaving)
x86-TSO: store buffer reordena Store→Load → Dekker r1=r2=0
HW: mfence (StoreLoad) o RMW (xchg, lock cmpxchg) · ARM: dmb, acq/rel
JMM: data race sin garantías · programas DRF ⇒ SC
JIT cachea la variable → while(x!=id); nunca termina
Java: volatile (visibilidad + no reordena) · arrays: AtomicIntegerArray
funciones atómicas en Java → synchronized / Lock
lo que valía en (b): vale solo con volatile/fence
lo que fallaba: sigue fallando (SC ⊆ TSO) + motivos nuevos
```
### Dorso, columna derecha
```text
# EJ 4 · linealizable: PL dentro del intervalo, orden por PL válido
CAS loop: while(T){ v=x.get(); if(x.CAS(v,v+1)) return }
inmutable: while(T){ o=r.get(); if(r.CAS(o, new E(..))) return }
marcable: s=c.next.get(mk); c.next.CAS(s,s,F,T)  (marcar)
sellada: o=top.get(st); top.CAS(o,n,st[0],st[0]+1)
# FINA remove (hand-over-hand)
head.lock; pred=head; curr=pred.next; curr.lock;
while(curr.key<k){ pred.unlock; pred=curr; curr=curr.next; curr.lock }
if(curr.key==k) pred.next=curr.next ←PL; unlock ambos
OPTIMISTA: recorrer sin lock; pred.lock; curr.lock; if(validate)...
   validate: desde head, pred alcanzable && pred.next==curr
LAZY validate: !pred.m && !curr.m && pred.next==curr
   remove: curr.marked=T ←PL; pred.next=curr.next
   contains: while(c.key<k) c=c.next; return c.key==k && !c.marked
LOCK-FREE find: curr marcado → pred.next.CAS(curr,succ) o retry
   add: w=find; if(curr.key==k) F; pred.next.CAS(curr,n,F,F) ←PL
   remove: curr.next.CAS(succ,succ,F,T) ←PL; pred.next.CAS(curr,succ)
# COLA 2 LOCKS
enq: enqL{ while(size==cap) wait; tail.next=e ←PL; tail=e;
   if(size.getAndInc()==0) wake }; if(wake) deqL{ notEmpty.All }
# COLA MICHAEL-SCOTT
enq: last=tail; next=last.next; if(next==null){
   if(last.next.CAS(null,n)) ←PL { tail.CAS(last,n); return } }
   else tail.CAS(last,next)   (helping)
deq: if(first==last){ if(next==null) throw ←PL; tail.CAS(last,next) }
   else { v=next.val; if(head.CAS(first,next)) return v ←PL }
# PILA: push: n.next=top; top.CAS(old,n) ←PL (+backoff)
pop: old=top; if(null) throw; top.CAS(old,old.next) ←PL
DOUBLE COLLECT: a=col; loop{ b=col; if(a==b) return Σb; a=b }
swap: lock[min]; lock[max] · optimista: leer(v); computar; lock; if(ver==v)
wait-free toda · lock-free alguna · locks: deadlock/starv-free
lazy/LF contains wait-free · LF add/rem lock-free · opt/lazy: inanición
```

## Versión B — Checklist anti-errores
### Frente, columna izquierda
```text
# SEMÁFOROS — del enunciado al patrón
mismos juntos, excluyen a otro → LS por tipo + room
"a X no le molesta esperar" → prioridad al otro, sin molinete
"nadie espera para siempre" → LS + MOLINETE FUERTE compartido
"si hay X esperando, los nuevos Y esperan" → X retiene mol (1 X)
   o LS de los X sobre `leer` (varios X)
"esperar a N" / rondas → barrera de 2 molinetes
2+ recursos distintos → orden global / N−1 / romper simetría
k unidades del mismo pool → tomarlas bajo un mutex
"en orden de llegada" sin fuertes → paso de testigo
"si está lleno, se va" → contador bajo mutex
"combinación exacta de 2 cosas" → gestores + bools bajo mutex
hilo activo que controla (bote, barbero) → sem por rol que abre él
# CHECKLIST antes de entregar
□ ¿alguien duerme con un lock que necesita quien lo despierta?
□ ¿mismo orden de acquire en todos? (condición antes que mutex)
□ molinete: ¿retenido (frena) o de pasada (solo cruza)? ¿dónde?
□ LS antes o después del multiplex = quién cuenta para el otro
□ ¿un permiso lo puede robar otro grupo? → uno por destino/rol
□ ¿quién avisa y quién espera? el que hace la acción avisa
□ ¿el int hace falta o ya lo cuenta un semáforo?
□ fuertes donde piden sin inanición (mol, multiplex, mutex)
# JUSTIFICAR (siempre)
cada sem: qué representa + valor inicial + invariante
mutex: #enSC + S.V = 1 ⇒ a lo sumo 1
sin deadlock: orden total · nadie duerme con lo que otro necesita
todo acquire tiene su release en todos los caminos
inanición débil: traza fair donde siempre se cuela alguien
   fuerte: cota = los que ya estaban adelante en la cola
escribirlo: "asumo débiles" / "este es fuerte porque..."
traza de sobrepaso: A espera en s; s.rel; B recién llega y
   hace acq antes (barging); se repite ∞ → A nunca pasa
```
### Frente, columna derecha
```text
# MONITORES — checklist Mesa
□ todo wait dentro de un while (el despertado rechequea)
□ cada wait tiene quién lo despierte, DESPUÉS de cambiar el estado
□ signal si los que esperan son intercambiables; si no signalAll
□ una sola condición → signalAll siempre
□ loops y acciones largas en el thread, no en el monitor
□ ¿actualicé TODO el estado? (último, fin, contadores que bajan)
□ ¿resetear algo rompe el while de otro? → fase / número de ronda
□ ¿un recién llegado se cuela y roba? si piden orden → tickets
□ ¿alguien retorna false y reintenta en vez de esperar? busy wait
□ los que "esperan lo mismo", ¿esperan lo mismo? → separar
□ signal no tiene memoria: el hecho se guarda en una variable
□ al terminar el juego / cerrar: despertar a TODOS
# DEL ENUNCIADO AL PATRÓN
orden de llegada / no colarse → tickets (miT, turno)
liberar N juntos → liberadosHasta += N
rondas / "hasta que termine" → número de fase / charla
emparejar A con B → avisos por contador; varios → ticket de pareja
capacidad + tipos → while con condición compuesta
preferencia → ifs en orden de preferencia después del while
"no dos veces seguidas" → while(último==yo && !fin)
no perjudicar pedidos grandes → tickets: solo el primero toma
# JUSTIFICAR
mutex: lo da el monitor
sin deadlock: todo el que espera tiene quién lo despierte
inanición: con tickets no hay · Mesa sin tickets: se cuelan
signal vs signalAll: decir por qué
# HOARE (inciso b)
signal cede el monitor en el acto ⇒ la cond sigue cierta ⇒ if
vale si solo se señala con la cond cierta y despierta uno
signalAll o señal "por las dudas" ⇒ sigue haciendo falta while
el que señala espera en la cola urgente (prioridad sobre entrada)
```
### Dorso, columna izquierda
```text
# EJ 1 — procedimiento
1 propiedades en orden: MUTEX → DEADLOCK → INANICIÓN (=GdE)
2 buscar: ¿marca antes o después de chequear? ¿turno? ¿x++? ¿for?
3 (a) no atómico: desagregar tmp=x; x=tmp+1 y entrelazar
4 (b) atómico: cada llamada es 1 paso; rehacer el análisis
5 "vale": invariante o absurdo · "no vale": traza en tabla
6 inanición: traza INFINITA y FAIR (un ciclo)
# FALLAS TÍPICAS → qué rompen
chequeo antes de marcar → MUTEX (check-then-act)
marcar antes de chequear, sin desempate → DEADLOCK/livelock
turno estricto → INANICIÓN (el otro se queda en la SNC)
ticket decrementado / turno sin reset (si reentran) → MUTEX
elegir siempre el menor id → INANICIÓN de los ids altos
dos llamadas atómicas separadas → otro se mete en el medio
función con for no atómica → entrelazado dentro del for
Peterson con otro=(id+1)%n, n>2 → MUTEX
Bakery sin desempate por id → DEADLOCK
ref: Peterson flag[i]=T; turno=o; while(flag[o] && turno==o)
# (c) MEMORIA — respuesta modelo
supuse SC. En la realidad: x86-TSO reordena Store→Load
   (store buffer) y la JMM reordena/cachea si hay data races
lo que valía en (b) sigue valiendo solo si agrego:
   lenguaje: volatile en compartidas (arrays: AtomicXArray)
   arquitectura: fence StoreLoad (mfence) o RMW atómico
lo que fallaba sigue fallando (SC ⊆ TSO) + motivos nuevos
   (visibilidad → while infinito, reordenamientos)
la arquitectura nunca arregla lo que ya falla bajo SC
# DEFINICIONES
deadlock: todos esperan · livelock: giran sin progresar
inanición (GdE): uno nunca entra aunque el sistema progrese
fairness débil: instrucción continuamente habilitada se ejecuta
traza: | paso | T1 | T2 | vars (con PC y locales T1.tmp) |
```
### Dorso, columna derecha
```text
# EJ 4 — kit para regular
LINEALIZ.: cada op pasa de golpe (PL) dentro de su intervalo;
   ordenando por PL se respeta el tiempo real y es válido
SC no respeta tiempo real ni es composicional; lineal. sí
# RECETA DEL PL
1 función de abstracción (qué valor abstracto representa)
2 modifica: paso atómico donde cambia el valor abstracto
3 lee o falla: la lectura que decide el resultado
4 separar éxito y falla
5 chequear: dentro del intervalo · atómico · estado coincide
PLANTILLA: "op se lineariza en <línea>, porque ahí <cambio>,
   y es atómico (<CAS / con lock>). op que falla en <lectura>.
   Ordenando por PL: ejecución válida de <spec> ⇒ linealizable"
NO linealizable: leer varios campos sin atomicidad
PL puede ser un paso de otro thread (contains lazy que falla)
# PROGRESO
wait-free: toda op en pasos finitos (1 lectura, recorrer sin retry)
lock-free: alguna termina; mi CAS falla ⇒ el de otro tuvo éxito
deadlock-free: locks en orden total · starv-free: + locks fair
optimista / lazy (validar y reintentar): NO starvation-free
# RECETAS
granular fina: lock por parte, orden creciente; "todo": todos
lock-free: CAS loop · varios campos: inmutable + AtomicReference
double collect: iguales ⇒ snapshot (PL entre los dos)
   si los valores bajan / reset → versiones por celda (ABA)
LISTAS PL éxito: add pred.next=n (LF: CAS) · remove lazy/LF: MARCAR
fina (HOH): tomo el siguiente antes de soltar; lock del que borro
cola 2 locks: PL enq tail.next=e · deq head=head.next
   despertar al otro bando tomando SU lock (no lost wakeup)
cola MS: PL enq CAS last.next · deq CAS head · helping de tail
pila: CAS top · ABA sin GC → sello (AtomicStampedReference)
contador solo con inc de 1: get con 1 collect ya es linealizable
```

## Versión C — Por puntaje (recomendada)
### Frente, columna izquierda
```text
# SUPUESTOS: sem débiles · Mesa · sin spurious · colas no fair
# SEMÁFOROS enunciado → patrón
mismos juntos excluyen a otro → LS por tipo + room
nadie espera ∞ → + MOLINETE FUERTE compartido
X esperando frena a nuevos Y → X retiene mol / LS de X sobre leer
rondas → barrera 2 molinetes · 2+ recursos → orden global
k del mismo pool → bajo mutex · orden de llegada → testigo
lleno se va → contador + mutex · combinación → gestores
hilo activo (bote, barbero) → sem por rol que abre él (no LS)
LS: m{ c++; if c==1 room.acq } ... m{ c--; if c==0 room.rel }
MOLINETE de pasada: acq; rel · retenido: acq ... rel después
   sin inanición: esc: mol.acq; room.acq; mol.rel; E; room.rel
   puente: mol.acq; LS[d].entrar; mol.rel (el 1ro trabado lo retiene)
   multiplex después del LS · LS antes/después = quién cuenta
PRIOR. ESC: lector mutexP{ leer{ LS_L.entrar(escribir) } }; LEER
   esc: LS_E.entrar(leer); escribir.acq; E; rel; LS_E.salir(leer)
BARRERA: m{c++; if c==n t1.rel ×n}; t1.acq;
   m{c--; if c==0 t2.rel ×n}; t2.acq
TESTIGO: m{ s=S(0); p=vacía; add(s) }; if p s.rel; s.acq
   salir: m{ popFirst; sig=peek }; if sig sig.rel
PERMISO ROBADO: sem compartido por grupos distintos
   → uno por destino/rol (llegada[costa])
el que hace la acción avisa "terminé"; el otro espera
# CHECK
□ nadie duerme con un lock que necesita quien lo despierta
□ condición (notFull) ANTES que el mutex · k permisos bajo mutex
□ fuertes: mol / multiplex / mutex si piden sin inanición
# JUSTIFICAR: cada sem = qué es + invariante · mutex #SC+V=1
deadlock: orden total / nadie duerme con lo que otro necesita
inanición débil: traza fair con barging ∞ · fuerte: cota
availablePermits nunca para decidir (check-then-act)
```
### Frente, columna derecha
```text
# MONITORES (Mesa)
sem→mon  V: x++; signal(cx)   P: while(x==0) wait(cx); x--
while(!puedo) wait; cambio estado; signal / signalAll
thread: loop + acción larga AFUERA; monitor = métodos cortos
signal si son intercambiables · si no signalAll · 1 cond → All
signal no tiene memoria → el hecho se guarda en una variable
no resetear lo que miran los while → FASE:
   miF=fase; c++; if c==n {c=0; fase++; All} else while(fase==miF) w
TICKETS: miT=prox++; while(miT!=turno || !puedo) w; ...; turno++; All
LIBERAR N: miT=prox++; while(miT>=lib) w · liberar: lib+=N; All
   liberador que espera: while(prox-lib<N) w(pLib) (esperar avisa)
RENDEZVOUS en 3 avisos (barbero):
   cli: esp++; sig; while(llam==0) w; llam--; while(term==0) w; term--
   pel: while(esp==0) w; esp--; llam++; sig · terminar: term++; sig
   varios peluqueros → emparejar (ticket)
rondas de sala: número de charla; el que cierra pone gente=0
"no 2 seguidas": while(ult==yo && !fin) w · fin → All a todos
recurso k: while(cola<k) w; signalAll · justo: tickets
bote: bool subiendo + orilla; la autorización se gasta al partir
# CHECK
□ cada wait tiene quién lo despierte · actualicé todo el estado
□ nadie hace return false para reintentar (busy wait)
□ ¿un recién llegado se cuela? si piden orden → tickets
# JUSTIFICAR: mutex automático · no deadlock: todo wait tiene
   despertador · inanición: con tickets no; Mesa sin tickets sí
# HOARE: signal cede ya ⇒ while → if (si solo se señala con la
   cond cierta y despierta uno) · signalAll / "por las dudas" ⇒ while
# MÁS
pizzas: while(g==0 && ch<2) w; if(g>0) g-- else ch-=2
secuenciador: while(t!=n) w(c[n]); f(); t=(n+1)%3; signal(c[t])
1 sola condición (inciso b) → todo signalAll
Atrapador sin bloquear: if(prox-lib<N) return; lib+=N; All
```
### Dorso, columna izquierda
```text
# EJ 1 · MUTEX → DEADLOCK → INANICIÓN (=GdE), en ese orden
SC termina · SNC puede no terminar · inanición = traza ∞ FAIR
(a) no atómico: desagregar tmp=x; x=tmp+1 y entrelazar
(b) atómico: cada llamada = 1 paso · "vale": invariante/absurdo
traza: | T1 | T2 | estado (PC, vars locales) |
# FALLAS TÍPICAS
chequeo antes de marcar → MUTEX (check-then-act)
marcar antes de chequear, sin desempate → DEADLOCK/livelock
turno estricto → INANICIÓN (el otro en la SNC)
ticket decrementado / turno sin reset (si reentran) → MUTEX
elegir siempre el menor id → INANICIÓN
2 llamadas atómicas separadas / for no atómico → meterse en medio
Peterson (id+1)%n con n>2 → MUTEX · Bakery sin desempate → DEADLOCK
# REFERENCIA
Peterson: flag[i]=T; turno=o; while(flag[o] && turno==o); SC; flag[i]=F
Bakery: elig[i]=T; num[i]=1+max; elig[i]=F;
   ∀j: while(elig[j]); while(num[j]!=0 && (num[j],j)<(num[i],i))
# (c) MEMORIA — respuesta modelo
supuse SC · x86-TSO: store buffer reordena Store→Load
JMM: con data races reordena y cachea (while(x!=id) infinito)
lo que valía: solo con volatile (arrays: AtomicIntegerArray)
   y fence StoreLoad (mfence) o RMW atómico (xchg, cmpxchg)
lo que fallaba: sigue fallando (SC ⊆ TSO) + motivos nuevos
la arquitectura nunca arregla lo que falla bajo SC
funciones atómicas en Java = synchronized / Lock
DRF ⇒ SC (sin data races, la JMM garantiza SC)
# DEFINICIONES
deadlock: todos esperan · livelock: giran sin progresar
inanición (GdE): uno nunca entra aunque el sistema progrese
fairness débil: toda instrucción continuamente habilitada corre
```
### Dorso, columna derecha
```text
# EJ 4 — kit para regular
LINEALIZ.: cada op pasa de golpe (PL) dentro de su intervalo;
   ordenar por PL respeta tiempo real y es válido secuencialmente
# RECETA PL
1 función de abstracción · 2 modifica: donde cambia el valor
3 lee/falla: la lectura que decide · 4 éxito ≠ falla
5 dentro del intervalo · atómico · el estado coincide
"op se lineariza en <línea> porque <cambio>; es atómico
   (<CAS / lock>); ordenando por PL es válido ⇒ linealizable"
leer varios campos sin atomicidad ⇒ NO linealizable
# PROGRESO
wait-free: toda op finita · lock-free: alguna (CAS falla ⇒ otro ok)
deadlock-free: locks en orden · starv-free: + locks fair
optimista / lazy (reintentan): NO starvation-free
# RECETAS
fina N partes: lock por parte, orden creciente; "todo": todos
   swap(i,j): lock[min]; lock[max] · PL con todos tomados
optimista: leer; computar sin lock; lock; validar versión; reintentar
CAS loop: while(T){ v=x.get(); if(x.CAS(v,v+1)) return }
varios campos: objeto inmutable en AtomicReference + CAS
double collect: 2 collects iguales ⇒ PL entre ambos
   valores que bajan / reset → versiones por celda (ABA)
# PL DE ESTRUCTURAS
listas: add pred.next=n (LF: CAS) · remove lazy/LF: MARCAR
   falla: lock + validación ok · contains lazy: nodo sin marcar
cola 2 locks: enq tail.next=e · deq head=head.next
cola MS: enq CAS last.next · deq CAS head · vacía: lee next
pila: CAS top · ABA sin GC → AtomicStampedReference
lazy/LF contains wait-free · LF add/remove lock-free
contador solo inc de 1: get con 1 collect ya linealizable
```

