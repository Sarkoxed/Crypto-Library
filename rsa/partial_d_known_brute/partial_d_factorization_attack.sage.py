

# This file was *autogenerated* from the file partial_d_factorization_attack.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_256 = Integer(256); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_5428319796045211049429895615786180214806332412433908118912944105933799755924048356596668364830017530316168005501956987750004678902378258368628660587576370389316775011201104633814960380997330149311988874973533865630161979248277661983596804506447941602246373409516525334571769375662832082044612653054661386486557899727683409333356513003513809817053744306020678454254492345080054190372864501806381782735846600890755861890212923924119058571107334432987249173507040097860877717939269543480315898382579759088566837119599401286204979572507572415056975713824044173753717716941432260321837506965356367188847247284026163171001767657470732753298187862740683884903395921458637850765819795521383188032180835149588151634686535205180923997813923640032483717235057394926317585823939407422711848478221633846024925038668812593747674275366426479371911818470469555510459837995191365994726614426414176735967021949914608139176142745777832340530861 = Integer(5428319796045211049429895615786180214806332412433908118912944105933799755924048356596668364830017530316168005501956987750004678902378258368628660587576370389316775011201104633814960380997330149311988874973533865630161979248277661983596804506447941602246373409516525334571769375662832082044612653054661386486557899727683409333356513003513809817053744306020678454254492345080054190372864501806381782735846600890755861890212923924119058571107334432987249173507040097860877717939269543480315898382579759088566837119599401286204979572507572415056975713824044173753717716941432260321837506965356367188847247284026163171001767657470732753298187862740683884903395921458637850765819795521383188032180835149588151634686535205180923997813923640032483717235057394926317585823939407422711848478221633846024925038668812593747674275366426479371911818470469555510459837995191365994726614426414176735967021949914608139176142745777832340530861); _sage_const_36615285368609217027990696832219564975645396025839448603550722215528831777944277409184209746569508382000117685572373266576553506653334128272745395833722704019808593828580820111936508055515989069793827759232889054006519571304141347557173463617496117933908190447821763116123888708454908558173851270724487683707203128781744328187866932288167101072782678623706752493156936531030049632294000001216448588870813054219299638364524292187215868496427499685775066924022167414278944122220389502297700893742402514777343705362980603647402791920660046135649818722215742983682637111126146288516558126061194385853943902373016482873890527181612091943551251140940159221108138996782997505927393128272144981129076563222770165407235223160219546914795399387681517783789257295572397664769977615633153216680363798233602257124403376457767456852623099406810750439289989681027629030287535926662227551557991850095852342012098548743139230558994356723 = Integer(36615285368609217027990696832219564975645396025839448603550722215528831777944277409184209746569508382000117685572373266576553506653334128272745395833722704019808593828580820111936508055515989069793827759232889054006519571304141347557173463617496117933908190447821763116123888708454908558173851270724487683707203128781744328187866932288167101072782678623706752493156936531030049632294000001216448588870813054219299638364524292187215868496427499685775066924022167414278944122220389502297700893742402514777343705362980603647402791920660046135649818722215742983682637111126146288516558126061194385853943902373016482873890527181612091943551251140940159221108138996782997505927393128272144981129076563222770165407235223160219546914795399387681517783789257295572397664769977615633153216680363798233602257124403376457767456852623099406810750439289989681027629030287535926662227551557991850095852342012098548743139230558994356723); _sage_const_0x10001 = Integer(0x10001); _sage_const_10 = Integer(10); _sage_const_1337 = Integer(1337)
from random import randint

def brute2b2(n, g, d, e, k=_sage_const_2 ):
    t = d * (_sage_const_256  ** k) + _sage_const_1 
    k0 = e * t - _sage_const_1 
    prec = []
    while k0 % _sage_const_2  == _sage_const_0 :
        k0 //= _sage_const_2 
        g0 = pow(g, k0, n)
        gc = gcd(g0-_sage_const_1 , n)
        if gc != _sage_const_1  and gc != n:
            return gc
        prec.append(g0)    
    print(len(prec))
    
    effg = pow(g, e, n)
    
    for i in range(_sage_const_2 , _sage_const_256 **k, _sage_const_2 ):
        extrapow = i
        c = _sage_const_0 
        while extrapow % _sage_const_2  == _sage_const_0  and c < len(prec):
            extrapow //= _sage_const_2 
            t = (prec[c] * pow(effg, extrapow, n)) % n              
            gc = gcd(t-_sage_const_1 , n)
            if gc != _sage_const_1  and gc != n:
                return gc
            c += _sage_const_1 

n = _sage_const_5428319796045211049429895615786180214806332412433908118912944105933799755924048356596668364830017530316168005501956987750004678902378258368628660587576370389316775011201104633814960380997330149311988874973533865630161979248277661983596804506447941602246373409516525334571769375662832082044612653054661386486557899727683409333356513003513809817053744306020678454254492345080054190372864501806381782735846600890755861890212923924119058571107334432987249173507040097860877717939269543480315898382579759088566837119599401286204979572507572415056975713824044173753717716941432260321837506965356367188847247284026163171001767657470732753298187862740683884903395921458637850765819795521383188032180835149588151634686535205180923997813923640032483717235057394926317585823939407422711848478221633846024925038668812593747674275366426479371911818470469555510459837995191365994726614426414176735967021949914608139176142745777832340530861 
part_d = _sage_const_36615285368609217027990696832219564975645396025839448603550722215528831777944277409184209746569508382000117685572373266576553506653334128272745395833722704019808593828580820111936508055515989069793827759232889054006519571304141347557173463617496117933908190447821763116123888708454908558173851270724487683707203128781744328187866932288167101072782678623706752493156936531030049632294000001216448588870813054219299638364524292187215868496427499685775066924022167414278944122220389502297700893742402514777343705362980603647402791920660046135649818722215742983682637111126146288516558126061194385853943902373016482873890527181612091943551251140940159221108138996782997505927393128272144981129076563222770165407235223160219546914795399387681517783789257295572397664769977615633153216680363798233602257124403376457767456852623099406810750439289989681027629030287535926662227551557991850095852342012098548743139230558994356723 
e = _sage_const_0x10001 

for i in range(_sage_const_10 ):
    g = randint(_sage_const_0 , n - _sage_const_1 )
#    g = 763799206740273132866147383133639529947404600887562098126666937635213618696132050762186996267690547009080776958153872780212047506769558443674217225924031921552643775244162720093251972978448688159542903520998782775563713553352991867736484174624991162888864189508587226984970177106803871955008862454612288851239586989428713518033559800926655279267592131177040887229124712836277513173211098758788583103517043939675458400233545861533782979381013756748039928099834001439496217320648999050197890228835955736174126761795993453300903368159065045511262025467887211366418676644610169909817861603162427372702677787949476449824552325718330763703476958029642567076031849129951029181705097352258685014350487261214348491749716252918755597364325395616422067034953974596273273304799047025299701566962571632018474746185050608882617228223157636144040586640496550966410323341775122955451132030166077854435998537800098007316637621011575051645311
    try:
        p = brute2b2(n, g, part_d, e, k = _sage_const_2 )
        q = n // p
        assert p * q == n
        print("got it")
        exit(_sage_const_1337 )
    except Exception as ex:
        print(ex)
        continue
