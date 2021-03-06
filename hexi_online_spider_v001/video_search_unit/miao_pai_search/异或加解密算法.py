# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/9/16
def encode(plaintext,key):
    key = key * (len(plaintext) // len(key)) + key[:len(plaintext) % len(key)]#取整数/余数
    ciphertext=[]
    for i in range(len(plaintext)):
        ciphertext.append(str(ord(plaintext[i])^ord(key[i])))
    return ','.join(ciphertext)
#解密
def decode(ciphertext,key):
    ciphertext=ciphertext.split(',')
    key=key*(len(ciphertext)//len(key))+key[:len(ciphertext)%len(key)]#取整数/余数
    plaintext=[]
    for i in range(len(ciphertext)):
        plaintext.append(chr(int(ciphertext[i])^ord(key[i])))
    return ''.join(plaintext)

# 秒拍解密
def _decode_resp_content(resp_content):
    """解密请求响应的数据
    :param resp_content: 请求响应的content"""

    def bytes_to_int(data, offset):
        result = 0
        for i in range(4):
            result |= (data[offset + i] & 0xff) << (8 * 1)
        return result

    def reverse_bytes(i):
        return ((i >> 24) & 0xFF) | ((i >> 8) & 0xFF00) | ((i << 8) & 0xFF0000) | (i << 24)

    if len(resp_content) <= 8:
        return ''
    dword0 = bytes_to_int(resp_content, 0)
    dword1 = bytes_to_int(resp_content, 4)
    x = 0
    if (dword0 ^ dword1) == -1936999725:
        x = reverse_bytes(dword1 ^ bytes_to_int(resp_content, 8))
    buffer_size = len(resp_content) - 12 - x
    if buffer_size <= 0:
        return ''
    else:
        buffer = bytearray()
        for index in range(buffer_size):
            buffer.append((resp_content[8 + index] ^ resp_content[12 + index]) & 0xff)
        return buffer.decode('utf8')
if __name__ == '__main__':
    plaintext = """#H�;=�]G�(r0�I.E�yt�*�<vg�ZF�/s3�/F�r"�(�cta�ZMX�/{=�I'H�{F.�qH�o-=�	^�|)8�uM�*Et�_q�o-d�
\�/d�Hs�~K%�~�n"d�Y�,}a�_M�~-(�
HL�k<n�Z	X�h=h�YD�=a(�Iw�=e�NG9�beL�
-�QyY�%*�?�=Ss�X7Q�hs�w�dz�F9J�dU#�&|�nS�Li"�n
M�o#�p0@�^4�?n�\u�9o�_`�}9P�_L#�-n�l�k?V�	�mlZ��RW^�"�Kjc�9:�JUr�hyP�;�;8g�]�P(6�3Jj��Y
 �Gq�U	�Zh�h�1ci�y6�L$�z7�N$�`N~�Bb\�`Xl�B4�+Z\�J79�pT�Jb�'~R�Jp�<-�XHg�bxK� 9�huX�JOz�svJ�CGg�reK� 8�4:�A+�qS^�Cch�6Z\�P)�e5� z�!\�Gll�2Y]�(�b`�V)�v
\�C3?�6�UZ~�dk�^*�)_�O2n�c�q-�$-X�o�b(
�t�dDM�81{�	U'�0c�l!�_w�}f�q�rS5�^qS�2<�WoO�4 :�@" �l mi�W
c�9~A�	m�df�;x�Z B�!7�MmV�oW-�2C�wZa�EbW�g>�}�"D.�fF�g.�E;�}b�_{�,Y1�5�,]g�\g;� HR�g)>�\P�z2~�S�r:?�Wc�t:�I^�$$�In*�?M�;I'�W`�+�SRx�<!�[L_�h+ �7mP�I2d�#B�`t�mV�Ox"�?B~�cm�{�}y�;�pvT�z�~r&�G�rl�GY�*Ko��Xlb�4Z%�eR�0w=�hd�8i�E�TH�*!�]rC�^a�*�}Kg�_qE�+5�w*i�G�r.w�M�2 z�]P�s3t�/�N{x�TM�P �fL�
R�k^>�,
9q�0T�_$y�yW
�G=5�s\�Gld�"�Gh5�#
Ij�`E�g �y;�yZ�^O�(Q�yB�OQ�r�b^�D�|:U�e
2�pst�,+�z\�9q�1T�^$y�xW
�F=5�r\�Fld�#�Fh5�"
ps�}MB�M}p�|IE�H~q�%�Di*�vK�8i�>K�Jv;�Yg�q*�_Gb�07�Tl�B{�0~�l1K�.d&�)�oT�;8�Roi�%-<�J`d�-4�mk�24)�A[G�7>)�
rz�a�},�>Q�Q=b�&X�y;�O]�'c�B�1Xu�D6�~|�\k�=4}�IU_�.}�bB�`(�$M�Cx%�yJ�Uh`�1�-1�;�^ht�*JN�r~�6P�U#,�.@�#(�`S�O=�"h\�K)�(uG�E&�5}O�V"�y{O�<�1j�X S�3l�S�ji`�..0�`H�('$�JCj�}+�"Ht�R!+�|K[�^gy�;	�'a�uW[�Zt�7l�^`�=q�Po� y�Ck�l�u�$nL�M�&h^��m)�;*y�d�=#m�_G#�hb�7L=�G%b�iR�p+�p_�r>�gP�$p�5x_�2�{}[�8�`=U�R%�h|F� i�hA�!�"xH�t2#�0B�t z�GQ>�3�ok8�/Z�M\m�2�SSB�gl�| N�P":� G�1q�g^S�E(:�2[e�].�?�N$�-�	aI�3C8�|�Eu|�'9�S�v"'��hCI�;%k�U�`
r�yP�w[>�MyV�9	l�UC�e9!P@�x1)�^D�4-0�QL]�~8d�R2�|>v�MO2�%;�a|Q�Q2)�guE��2EJ�mk'�YTQ�70l�^Q�?8%�LQB�ugs�V�w0t��!0u�GC�"7q�@�7w)�R(Z�3E*�s�0F+��0Yr�V5�k!�G$L�}$�	v�&*1�UFS�8/2�HN[�+!6�RB�a3/�NG�'-@�LA�}0@�Ds�Q#�aM[�W
7�5ny�:8�]U�i+#�O�n.q�GW�|.0�E�&)d�GO�!ze�O�w|1�H�!|2�[�bW(�:X�2h� 9Y�5 m� & �fJa�[yS�w[?�MyW�9	m�UB�e9 PA�x1(�^E�4-1�QL\�~8e�R3�|>w�MO3�%; �a|P�Q2(�guD�
�2EK�mk&�YTP�70m�^Q�?8$�LQC�ugr�V�w0u��!0t�GB�"7p�A�7w(�R([�3E+�s�0F*��0Ys�V5�k �G$J�(Jh�
�q`�`�.;I�!�vFV�!>�=�wa�~�!2�2UW�Fwm�d[O�/m�(]�2�vU]�[dm�k�;c�y_A�[o�7Yj�M1�Il�s!8�'mr��MN(� l�D	w�6`�_i�e-5�P�a3�:Uo�\3^� Fk�1~7�U�Xm`�<�Xm�:�bzf�V�
jb�:	>�hZ�_c�n{?�VZ�
jo�:Z3�n�P3�e#o�]EY�0a�`R=�U�	A0�?wl�
�V`?�nTc�Xl[�n�f/2�^I
q#�yS�%*�LGh� .�NMu�` �P}�!3�}g�nJ�{$�T`F�aT �Y7C�8wa�i$�
>E�:w�XYF�alt�U^L�mm��+?n�B�}`%�?K�~Zi�\�7OW�\wo�)@
�Yb&�>H�[uj�jYH�+<�gJE�]ht�dXY�Uui�wYK�*(�t�=F�CHq�{x-�NJ�?*�sv�KmO�y�')%�LD�N9"�~Z~�KnO�y�q%�D�l*�{Zv�LoE�p�'+,�O�Lnx�xY$�Ki� �&}|�O�O:*�,v�m�:A1�H$P�r�G0h�E]�!}�
O�:K:�
|H�yr�VP]�;7<�RNI�1*'�\CF�,"/�OMB�`$/�A\�(�[)X�8q
V�=Qd� �cIg�&V�sr�?8x�LS�bl�>NN�R/7�'][�g �kE�1n�9mA�
2�t$_�K/�|eL�9c�eK)�G$Z�^9�^
ad�=QV�ec�8RW�U"1�4E�g �jE�1n�8mA�
^9�_
5�/Tx�@ �)Ow�u�me�c�o
:�}QO�Kc)�>V�Z
>�?(�[M~�/(!�[IU�(ko�I�h&{�7U�C |�yL�[%�>�7%�a[I�/,� �yu�g
�a$R�Tg�`)W�Tg�zr�X^5�zd�j�1f5�PP�j) �BE�6 3�X�6z#�F�px4�JI�( j�@D�b~)�[G�kv4�ZT�>1k�I�i={�Xa�nY:��*2}�IK�<2.�
�*4x�H�=;}�XQ�9k4�Q�nd%�Y8P�<Y3�{A�|5�t�#X5�L4Y�;Q+�d2D�
Ff�:jD�_-�,QN�Y?:�cG�Ab"� =F�T\d�'F�K)�i�9v�^q�d@&�HbQ�,9�.�:d�Sk�qQ8�A,�1Ew��]6�)B�-um� �cpi�
�x0g�_�pqt�-[�pL<��NAx� �&Fm�e�*&c�n@3�#U�]\�0B�lo�6?|�iR�lp�;�K9/�#M[�t�6x�Wp�"z�LT~�-;�Dm�)IB�D(%�7t
B�$Qm�W=�:Tn�J5�)Zj�)�cHs�L9>�'f�D_V�2�TzZ�<M�lS�
e-�Z.k��B5q�v
C�$Ql�W=�:To�J5�)Zk�)�cHr�L9?�'g�D_W�2�Tz[�<M�lR�
e,�Z.j��B5p�v
�8M�^|�E+I�v�C+$�^�'lM�	(�O|�|@�J%x�PM�tf�L )�u�tDM�@!u�T�,7O�V+�G#�uB�M'�
�s3C�JR{�'C�#�&'�HS�{dM�Nx�sM�%�&w�2
U�@o4�%k�Q)Q�d`�T+T�dv�k�d4`�@�'z%�U�jn1�P�lir�_Y^�305�W�{0l�\	�c9m�Y	A�5`*�F?I�3Q=�	a�j|��Pg�>wE�[g�a6
�BU�c#2�Y�,`{�Z �}/i�_K��n"I�Tx�O*6�X� cz�"?�:�b9\�Se)�d�7�!k
K�,?.�H	�.h)��$o5�T
R�x($�B�.vo�@)�-L#�t�<C,�a �in�vL�=Zn�T(�0Ic�
kR�3[�vM�#Zo�F)�|P�I2g�GP�%%�?�Ne
�yTV�2f�CGS�t#�A=�b�{QX�O4m�A�#"W�c�Jn[�+]�dd�O]�v �F1�L3	�zUU�O36�F �r~\�JMi�haK�*� &v�E�J0!��
�3/�tJ�aVp�	"�3~+�F�}{/L�f;!�TQ�nz2�&�nGz�U�dP�e�Os�:<d�[}�,MH�B$�Q>�r�>E-�a}�>0S�[R#�wpJ�8�bv]�XT5�,$�x �nA�f4�dZ�	k;�y
R�e?�5R�Ri!�}3X�?_2�Ms�&"�Lg�:Z�`/~�W[.�
C�Z[�]�U^�{4r�YI^�-0.�
�/2� A�)d�r8�.<_�B^q�+?�JV0�%;l�VO�7"B�m[	�1X�Dp*�|e�Qd$��q}}��T@C��+ll�	�p'd�H�xng�	Z�#8j�E]�#<4�ZQ�#o5�
� 8g�\�f5k�9F�T6"�b�W7&�n�Hna�$�=$�5P�8r�g.�;-I�WOg�>�_G&�0*z�C�"3T�xJ� N�Qa<�is�Du2��dlk�<�AQU�
�d~i�; �^0:��qu}�"�zkO�m�OB�m*�2]�U5n�oB�j!�wN�U95�!\M�fo�/D�[f9�wDU�fo�mC�Oh.�+J�O)A�"j$�n@�?Mx�K(M�'�3&v�
T�ty7�	C�rga�P;�h%�6G�+j2�MR�8d<8I�>Yz�Kl�{0i�]�818�	mM�0^(�EjN�$6;�
�a33�VoF�0Yt�Ea�tAK�L'/�R�"bF�Rv�F'@�pD�Itz�M�$9�_$�M*�)L�*t�B_A�r9�G_,�es�o�rr0�P
�2f;�R�2~-�WH�2M;�S9N�q~�Sv�<j�Oc�:)�	 �eIn�kT�-I7�A%R�5@6�p�cq�F�e(f�_U�j5w�X�k,iC�|a&�LU
�/:g�JT�,8r�B�,w1�^U�|&~�D�.`&�YT�=X"�ms�Z �j-�H]�!b6�@j�,uY�p l�G10�qV�-qc�HA�;)7�OHE�uj-��.F8�C!Y�*X,�I<B�$U#�T4J�7['�.T�j=�ma�3	�Dq� 1�pwV�3�wDZ�(/=�EM�$io�S_�$?0�MQo�,<
�?�'+�9�%.[�	<�ghY�ERh�g0�Xe�jz_�[Cf�vsW�FBu�d&�*�[q�nO�V z�
UO�:1�W$�S"�0@�s"�X�h4M�]U~� J�4�%s�^PD�h1�W(�R"�cA�U+'�	^�9gM�S}�/qQ�N4�l9�@d�,z�C2�s8�T|�k1�4Ra�Z&C�j
�}pp�_	�:&3�LOW�#m{�U�&[}�S5	�i8�X0	�tz�vX�?;�x�>3�fb_�:�H"�en4�:L�J y�U�fw1�D�fqg�K;�Jd\�&r�Og�.3�Aco�2�SzA�-*� h*�j
u�B?W�`Ru�B:�2 ]�n/:�M�k,{�
EU�e(	�\{�w1'�	a~�$#L�NAu�+F�rn�'?�E4p� C�.s�1X�Ue{�4
�],x�4KE� zq�2BB� {!�c�W&r�c�% �c�|~�H
�%7�O�&~3�J�9't�UF�ft1�D�fpg�J;�Je\�&r�Of�.3�Abo�2�S{A�-+� i*�j�8a �V$h�KY�a~�	e�*d�p�q/�@m�yf�#�$0�$�$1G�GUp�sl�GZp�#oF�G_u�36�lEl�5Q�7a�4U�; b�m�qu�B>W�`T$�v�fj�\^E�s96�[�px+�VH�t
�ka}�CG�Soe�! �Eu_�*2�Dl�1m�=Y�b.g�F�?v?�S\�'p3�JH�q/0�S�7~�D�:%t��q%"�@�=h>�S�{9i�	
!�{ry�H1*� VA�Veu�`+>�sH�rB�Pn#�5@�\m4�3�_c�)gR�\R0�jE�6|�yN�O];�-l
�XZl�l�	e|�|PE�O0�wo�Z<�5I�S0*�&VL�E
�Qm�!aU�TY1�gD�Tf'�!_�Dj�ug_� Rf�a�o �rX�b�&1 �
c�or�-v�)G�%v�-D�5 �mPT�2# �FVS�|f�	�hrL�8�o1�_ �6vE�Lu�6/�ZJy�?.[�y�fi�9
s�W~Q�cRs�?�bKm�$�u"�Y$A�4I$�@B�!q`�]B�b80�XC�-*v�2�{ps�K)8�{Nn�)L�=G%�Ve�
*�l v�[@�ey�aV%�W7�B,�jzp�SL�9 �6Z�;t�`Z�Zxn�T�T{�l3�Jo�f.�G`�{&	�Id�7<�E~�*"�IF@�-~r�K�!x$�KF�{}%�CD�&""�y�L!#�u�E'4�5@�64�&�I}��s1$�E�t:!�V�3xg�AZ]�mx?�W�~uu�\DL�li|�AYM�m{)��<D~�!K�~�H
�-.9�XX�jD-�Zt�/Az��,+8�Y	�8O|�YvN�,B(�]�z)n�]�?>q�^L�|v6�	C�9p�\(� ] �fm|�S^M�+x�?Z�k?�|V�=l�>
�Rse�7�Tnc� LY�n4�hU�7d:�Y�im4�@�[l!�:N�Aln�-�9t�c\�48�%�{b�s@�B!x�n�dx�%^O�#c�eJ �Gp{�+RA�C&5�yz�Vw�7�B}�,?�MP`�$~�I",�=PI�Pf�gM_�6=�QWz�(�}pd�.C�yve�
�6dy�F^%�qB�vl�r�~-�vq�b�o_�@X�*	n�hn�V�eB#� �RF%�g4P�
/l�l[�Na)�lY�u=�p\�r~�6BR�Z+9�>	�+`�~G�
Gf�/>�AiI�cEk�$�g%�rQ�5.~�G�{+z�E�`kt��h*g�vH�v:�pU�C_=�
�of=�MI�=4�a|�z�~�aP�r ?�i�|M�i,�pp�	Q�dT�G#�w(d�/gP�I>�mg�^>?�G�`3�}Q�5Qs�[%�7Du�~W�a
�B4�/ �KF5�("�Fm�~p	�V}�u3"�RO�<cy�QL�8du�PS�6?��:'.�IH@�sj(��(F=�[*_�6C>�F"W�%M:�
�0oj�
	Y�x?a�Ic�+"�^9D�ge1�Q]�$i`�5�"&�W0�`l`�\�shf�4�#$�V3�nog�	^�y?j�Oc�~~�1�;mn�^YV�+on�3�*/�_<�=`j�[�# 8�FAL�"-� $�6$� )�,q�@n�q�kh�QX.�$(B�EL�1-i�BS�r#q�H�9r$�K�wt(�
�dj+�-a�sk(�}�_Q�&@�9
b�Pi	�jKU�]~g�Q�2<`�

R�<2k� ]�""<�CV]�al��I7S� Z4�L3M�"P)�=@�cM!�M.N�;�ts�x�8b�|X�Lu�i�pY$�IS�B8�clR�N~�rlD�^N(�9'F�WF+�u|	�LM<�-|�Hn�9dL�\
(�.(�
p�p~�:�36�3�.+�	f�qjD�S61�a W�51�'iD�DY"�1nD�21�0 	�E8o�|d� #�l4E�\h0�hYS�n5�*2@�O
v�:?B�c7�7 S�B5j�&i�Y}�dnK�P2>�e�4m�!h�CP(�6dM�TO�cz"�?>K�0Z�l/I�U�`+p�	\�{9�]A�qci��rl?�B@�-,q�ZI�*l�k^N�[rl�>�MIf�8'�o� z
�A%n�5DL�n?n�S�zq;�X^�?i6�Z �)xw�M�w:+�[C�2+�E� 84�PQW�rk,�I�v=b�LaM� �dI�w
*�$G�xK7�eT�|9{�X�b3�7vQ�A4�9sV�@
�.o7�3�lTy�-�fIb� �{Aj�.�7Gj�P"�NL�=:�UsB�=;�rW�DXz�r66�9R�
v�9_)�5Y�5Hu�A1�c'�
oB�(C`�A&�Ex�p1Z�Bm�v)O� @+�:b`�W:�yd�C3�k`��2_�Gm}�e�Bd�p1F�(�11@�EAz�jU�q7�tV�y?�gR�He&�-K�h�`h�(U�gi�-�9~(�d�Dt]�wZ0�CeF�-{�D`�%	2�V`U�c7�Q0Q�7i�0
�7o�<	�gY?�^?�xKe��|yf�MOV�zg�JCS�e>�	_�$:m �2:h�FJR�i}�z�w~�r�dz�Kn�.c�c6�c@�+^8�dA�&-�:u �L�Gu�tQ�@nn�.
S�Gk<�&�Uk}�`	�R;y�4
a�bX�x*�pv�@�o6F�!N�o7x�Y[*�
vY�d:
� O�.i<�@VJ�.2w�GS�&:>�USY�`1;�R]�42e��46c��dj3�] �{xi�'�Jj�N|Z�|Ik�Ip_�|R"�!~ �Ni�=,S�` q�"K�Ii�'`�Fo�(gM�SE+�: E�I)�"�yG'�5N�qQ=�>P�wP$�My�a)�vf�|�^+>�|GQ�38�s�Qeg�%G]�k�f]�K.m�{O�em�8T]) �u

"""

    print(plaintext.encode())
    print(decode(plaintext,key="7b39758516002460160502434e5c514791eb6d8c44782e71955cd0f42e2fad"))
    exit(0)
    functions=input('输入A加密，输入B解密，其它关闭>>>>')
    if functions=='A':
        plaintext=input('请输入加密文字明文>>>')
        key=input('请输入加密密钥>>>')
        print('密文',encode(plaintext,key))
    if functions=='B':
        ciphertext = input('请输入解密文字明文>>>')
        key = input('请输入解密密钥>>>')
        print('明文',decode(ciphertext,key))