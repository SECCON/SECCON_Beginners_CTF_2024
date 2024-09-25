from Crypto.Util.number import long_to_bytes
import itertools
import gmpy2
import traceback
import sys

n = 28347962831882769454618553954958819851319579984482333000162492691021802519375697262553440778001667619674723497501026613797636156704754646434775647096967729992306225998283999940438858680547911512073341409607381040912992735354698571576155750843940415057647013711359949649220231238608229533197681923695173787489927382994313313565230817693272800660584773413406312986658691062632592736135258179504656996785441096071602835406657489695156275069039550045300776031824520896862891410670249574658456594639092160270819842847709283108226626919671994630347532281842429619719214221191667701686004691774960081264751565207351509289
e = 65537
cipher = 21584943816198288600051522080026276522658576898162227146324366648480650054041094737059759505699399312596248050257694188819508698950101296033374314254837707681285359377639170449710749598138354002003296314889386075711196348215256173220002884223313832546315965310125945267664975574085558002704240448393617169465888856233502113237568170540619213181484011426535164453940899739376027204216298647125039764002258210835149662395757711004452903994153109016244375350290504216315365411682738445256671430020266141583924947184460559644863217919985928540548260221668729091080101310934989718796879197546243280468226856729271148474
ab = 28347962831882769454618553954958819851319579984482333000162492691021802519375697262553440778001667619674723497501026613797636156704754646434775647096967729992306225998283999940438858680547911512073341409607381040912992735354698571576155750843940415057647013711359949649102926524363237634349331663931595027679709000404758309617551370661140402128171288521363854241635064819660089300995273835099967771608069501973728126045089426572572945113066368225450235783211375678087346640641196055581645502430852650520923184043404571923469007524529184935909107202788041365082158979439820855282328056521446473319065347766237878289


def decrypt(ans_x, aa, bb):
    try:
        ans_p = ans_x + aa
        ans_q = ans_x + bb

        phi = int((ans_p - 1) * (ans_q - 1)) % n
        d = pow(e, -1, phi)
        mes = pow(cipher, d, n)
        mes = long_to_bytes(mes)
        print(f"{mes=}, {ans_x=}, {ans_p=}, {ans_q=}")
        if "ctf4b{" in str(mes):
            print(f"flag: {mes}")
            sys.exit(1)
    except Exception:
        print(f"Error: {ans_x=}, {ans_p=}, {ans_q=}")
        print(traceback.format_exc())
        return


# This factorization can be got from factordb.
# cf. http://factordb.com/index.php?query=28347962831882769454618553954958819851319579984482333000162492691021802519375697262553440778001667619674723497501026613797636156704754646434775647096967729992306225998283999940438858680547911512073341409607381040912992735354698571576155750843940415057647013711359949649102926524363237634349331663931595027679709000404758309617551370661140402128171288521363854241635064819660089300995273835099967771608069501973728126045089426572572945113066368225450235783211375678087346640641196055581645502430852650520923184043404571923469007524529184935909107202788041365082158979439820855282328056521446473319065347766237878289
factored_ab = [
    3,
    173,
    199,
    306606827773,
    35760393478073168120554460439408418517938869000491575971977265241403459560088076621005967604705616322055977691364792995889012788657592539661,
    4701715889239073150754995341656203385876367121921416809690629011826585737797672332435916637751589158510308840818034029338373257253382781336806660731169,
]


for ii in range(1, len(factored_ab)):
    for partial_c in itertools.combinations(factored_ab, ii):
        tmp_a, tmp_b = gmpy2.mpz(1), gmpy2.mpz(1)

        for i in factored_ab:
            if i in partial_c:
                tmp_a = tmp_a * i
            else:
                tmp_b = tmp_b * i
        aa = tmp_a * tmp_a
        bb = tmp_b * tmp_b
        assert aa * bb == ab

        tmp_b = aa + bb
        tmp_c = ab - n
        ans_x1 = (-tmp_b + gmpy2.isqrt(tmp_b**2 - 4 * tmp_c)) // 2
        if ans_x1 > 0:
            decrypt(ans_x1, aa, bb)
