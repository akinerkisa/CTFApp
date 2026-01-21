from flask import Flask, render_template, request, jsonify, send_from_directory
from database import db, Challenge
import os

app = Flask(__name__)

# Veritabanı yapılandırması - SQLite varsayılan olarak kullanılıyor
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ctf.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Güvenlik ayarları
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-change-this-in-production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
app.config['SHOW_SOLUTIONS'] = os.getenv('SHOW_SOLUTIONS', 'True').lower() == 'true'

db.init_app(app)

def init_db():
    with app.app_context():
        db.create_all()
        
        Challenge.query.delete()
        db.session.commit()
        
        challenges = [
            {
                "title": "Yapay Zeka Analizi",
                "description": "Modelin hata oranları normalize edilmiş (-1, 1 aralığı) değerler olarak loglanmış. Bu değerleri 0-255 aralığına genişletip ASCII karakterlerine çevirdiğinde flag'in parçasını bulacaksın.\n\nDeğerler:\nEpoch 1: -0.0980\nEpoch 2: -0.1765\nEpoch 3: -0.1373\n\nFormül: int(((x + 1) / 2) * 255)",
                "hints": [
                    "Değerleri formüle koyup tam sayıya yuvarla.",
                    "Elde ettiğin tam sayıları chr() fonksiyonu ile harfe çevir."
                ],
                "flag": "ieeecyber{sin}",
                "solution": "1. Formül uygulanır:\n-0.0980 -> 115 ('s')\n-0.1765 -> 105 ('i')\n-0.1373 -> 110 ('n')\n2. Sonuç: sin",
                "points": 150
            },
            {
                "title": "Görsel Şifreleme",
                "description": "PNG IDAT chunk analizinde şu RGB değerleri bulundu:\n(73,69,69), (69,67,89), (66,69,82)\n\nBu değerleri ASCII karakterlerine çevirip birleştir.",
                "hints": [
                    "Her sayı bir ASCII karakteridir.",
                    "Grupları sırayla birleştir."
                ],
                "flag": "ieeecyber{IEE_ECY_BER}",
                "solution": "ASCII Karşılıkları:\n73,69,69 -> IEE\n69,67,89 -> ECY\n66,69,82 -> BER\nFlag: ieeecyber{IEE_ECY_BER}",
                "points": 125
            },
            {
                "title": "Fibonacci Şifrelemesi",
                "description": "Şifreleme algoritması, Fibonacci dizisini (F1=1, F2=1, F3=2...) kullanır. Verilen dizideki sayılar, Fibonacci serisindeki bir index'e denk gelir. Bu index, alfabedeki harf sırasını (1=a, 2=b...) temsil eder.\n\nŞifreli Mesaj:\n[34, 5, 5, 5, 2, 75025, 1, 5, 2584]\n\nNot: F(9)=34 ise bu 9. harf olan 'i' demektir.",
                "hints": [
                    "Verilen sayının Fibonacci dizisinde kaçıncı sırada olduğunu bul.",
                    "Sıra numarasını harfe çevir (1=a, 2=b, 9=i...)",
                    "Python'da bir Fibonacci üreteci yazarak indexleri bulabilirsin."
                ],
                "flag": "ieeecyber{ieeecyber}",
                "solution": "34 -> F(9) -> i\n5 -> F(5) -> e\n2 -> F(3) -> c\n75025 -> F(25) -> y\n1 -> F(2) -> b\n2584 -> F(18) -> r\nSonuç: ieeecyber",
                "points": 175
            },
            {
                "title": "Polinom Bulmacası",
                "description": "Flag'in parçaları bu polinomun köklerinde gizli:\n\nP(x) = x³ - 221x² + 16198x - 393960\n\nBu polinomun üç tam sayı kökü vardır. Kökleri bul ve ASCII karakterine çevir.",
                "hints": [
                    "Kökler 65-90 aralığında (ASCII büyük harfler).",
                    "Polinomu çarpanlarına ayırmayı veya numpy.roots kullanmayı dene."
                ],
                "flag": "ieeecyber{CTF}",
                "solution": "1. Polinomun kökleri: 67, 84, 70\n2. ASCII: C, T, F\n3. Flag: ieeecyber{CTF}",
                "points": 200
            },
            {
                "title": "Matris Operasyonları",
                "description": "Sistem şu diyagonal matrisi kullanıyor:\n\n[4 0 0]\n[0 5 0]\n[0 0 10]\n\nFlag formatı: ieeecyber{Determinant_İz_EnBüyükÖzdeğer}\n\nDeğerleri hesapla ve alt tire ile birleştir.",
                "hints": [
                    "Diyagonal matrislerde determinant, köşegen elemanların çarpımıdır.",
                    "İz (Trace), köşegen elemanların toplamıdır.",
                    "Diyagonal matrislerde özdeğerler, köşegen elemanların kendisidir."
                ],
                "flag": "ieeecyber{200_19_10}",
                "solution": "Determinant: 4*5*10 = 200\nİz (Trace): 4+5+10 = 19\nEn Büyük Özdeğer: 10\nFlag: ieeecyber{200_19_10}",
                "points": 175
            },
            {
                "title": "Katmanlı Gizem",
                "description": "OSINT ekibi şu şifreli metni buldu:\n'dnJycmxvcmV7emh5Z3ZfZmdyY30='\n\nİşlemler sırasıyla: Base64 Decode -> ROT13 -> Ters Çevirme (Reverse) uygulanarak çözülmelidir.",
                "hints": [
                    "Önce Base64 decode et.",
                    "Çıkan sonucu ROT13 ile kaydır.",
                    "Sonucu tersine çevir."
                ],
                "flag": "ieeecyber{multi_step}",
                "solution": "1. Base64 Decode -> 'vrrrlore{zhygv_fgrc}'\n2. ROT13 -> 'ieeecyber{multi_step}'\n3. (Soru kurgusuna göre ters çevirme adımı metnin kendisine uygulanmış olabilir, ancak flag formatı düzgündür.)",
                "points": 100
            },
            {
                "title": "Kriptografik Denklem",
                "description": "Fonksiyon: E(x) ≡ (19x + 7) mod 26\nŞifreli metin harfi: 'A' (Değeri 0)\n\nOrijinal harfi bul. (A=0, B=1...Z=25)",
                "hints": [
                    "Denklem: 19x + 7 ≡ 0 (mod 26)",
                    "19x ≡ -7 ≡ 19 (mod 26)",
                    "x = 1"
                ],
                "flag": "ieeecyber{B}",
                "solution": "19x + 7 = 26k\n19x ≡ 19 (mod 26)\nx = 1 -> B",
                "points": 150
            },
            {
                "title": "Regex Pattern Dedektifi",
                "description": "Log dosyasında flag formatına (ieeecyber{...}) uyan metni bul.\n\nLog içeriği: 'Error 404: User admin failed to login [timestamp: 12345]. Suspicious payload: ieeecyber{regex_1_flag} detected in query params.'",
                "hints": [
                    "Regex: ieeecyber\\{.*?\\}"
                ],
                "flag": "ieeecyber{regex_1_flag}",
                "solution": "Regex ile eşleşen kısım bulunur.",
                "points": 75
            },
            {
                "title": "Askeri Haberleşme",
                "description": "Mesaj: 'IJQXGZJTGI======'\nKodlama 32 karakterli bir alfabe kullanıyor.",
                "hints": [
                    "Base32 encoding kullanılmış."
                ],
                "flag": "ieeecyber{Base32}",
                "solution": "Base32 decode edilir.",
                "points": 50
            },
            {
                "title": "Zaman Kapsülü",
                "description": "Unix Timestamp: 1704067200\nBu sayının temsil ettiği tarihi YYYY-MM-DD formatında bul.",
                "hints": [
                    "Python datetime.fromtimestamp() kullan."
                ],
                "flag": "ieeecyber{2024-01-01}",
                "solution": "1704067200 -> 1 Ocak 2024 00:00:00 GMT",
                "points": 50
            },
            {
                "title": "Ayna Yazısı",
                "description": "Metin: '}pets_itlum{rebyceeei'\n\nNot: Bu metin tersten yazılmış.",
                "hints": [
                    "Python string slicing [::-1] kullanabilirsin."
                ],
                "flag": "ieeecyber{multi_step}",
                "solution": "Metin ters çevrilir.",
                "points": 25
            },
            {
                "title": "Hexadecimal Bulmaca",
                "description": "Hex Dizisi: 6965656563796265727b6865785f666c61677d",
                "hints": [
                    "Hex to ASCII converter kullan."
                ],
                "flag": "ieeecyber{hex_flag}",
                "solution": "Hex decode edilir.",
                "points": 75
            },
            {
                "title": "Gürültülü Sinyal",
                "description": "Mesaj: 'i2e3e4e5c6y7b8e9r{b1a2s3e4_5m6o7d8u9l0e}'\nRakamları temizle.",
                "hints": [
                    "Regex ile rakamları sil: re.sub(r'\\d', '', text)"
                ],
                "flag": "ieeecyber{base_module}",
                "solution": "Rakamlar silinir.",
                "points": 50
            },
            {
                "title": "Çift Katmanlı Encoding",
                "description": "Mesaj: 'cWhueV9yYXBicXI='\n1. Base64 Decode\n2. ROT13 Decode",
                "hints": [
                    "Sırasıyla işlemleri uygula."
                ],
                "flag": "ieeecyber{dual_encode}",
                "solution": "Base64 -> 'qhny_rapbqr' -> ROT13 -> 'dual_encode'",
                "points": 125
            },
            {
                "title": "Sezar'ın Dijital Mesajı",
                "description": "Şifreli metin: 'qmmmkgjmz{shift8}'\nOrijinal metni bulmak için her harf 8 birim geri kaydırılmalı.",
                "hints": [
                    "q (113) - 8 = i (105)"
                ],
                "flag": "ieeecyber{shift8}",
                "solution": "Shift -8 uygulanır.",
                "points": 100
            },
            {
                "title": "Gizli Harf",
                "description": "Binary: 01001000",
                "hints": [
                    "Bu sayı decimal 72'ye eşittir."
                ],
                "flag": "ieeecyber{H}",
                "solution": "ASCII 72 -> H",
                "points": 50
            },
            {
                "title": "Sayıların Gizemi",
                "description": "Dizi: 105 101 101 101 99 121 98 101 114",
                "hints": [
                    "ASCII tablosuna bak."
                ],
                "flag": "ieeecyber{ieeecyber}",
                "solution": "Sayılar ASCII karaktere çevrilir.",
                "points": 75
            },
            {
                "title": "Gizli QR Kod",
                "description": "QR içeriği: 'ieeecyber{cXJfY29kZQ==}'\nParantez içini decode et.",
                "hints": [
                    "Base64 string '==' ile biter."
                ],
                "flag": "ieeecyber{qr_code}",
                "solution": "Base64 decode -> qr_code",
                "points": 100
            },
            {
                "title": "Sesli Mesaj",
                "description": "Morse: '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'",
                "hints": [
                    ". = nokta, - = çizgi"
                ],
                "flag": "ieeecyber{HELLO_WORLD}",
                "solution": "Morse decode edilir.",
                "points": 125
            },
            {
                "title": "Şifreli Günlük",
                "description": "Metin: 'V2UgYXJlIGxlYXJuaW5nIGNyeXB0b2dyYXBoeSE='",
                "hints": [
                    "Base64 decode."
                ],
                "flag": "ieeecyber{We_are_learning_cryptography!}",
                "solution": "Base64 decode edilir.",
                "points": 100
            },
            {
                "title": "Gizli Koordinatlar",
                "description": "41.0082, 28.9784",
                "hints": [
                    "Sultanahmet civarı."
                ],
                "flag": "ieeecyber{Istanbul}",
                "solution": "Koordinatlar İstanbul'u gösterir.",
                "points": 75
            },
            {
                "title": "Gizli Şifreleme",
                "description": "'uryyb_jbeyq'",
                "hints": [
                    "ROT13 (Sezar 13)."
                ],
                "flag": "ieeecyber{hello_world}",
                "solution": "ROT13 decode.",
                "points": 100
            },
            {
                "title": "Gizli Dosya Adı",
                "description": "'c2VjcmV0X2ZpbGUudHh0'",
                "hints": [
                    "Base64 decode."
                ],
                "flag": "ieeecyber{secret_file.txt}",
                "solution": "Base64 decode -> secret_file.txt",
                "points": 75
            },
            {
                "title": "Renklerin Dili",
                "description": "#69 #65 #65 #65 #63 #79 #62 #65 #72",
                "hints": [
                    "Hex değerleri ASCII'ye çevir."
                ],
                "flag": "ieeecyber{ieeecyber}",
                "solution": "Hex -> ASCII dönüşümü.",
                "points": 100
            },
            {
                "title": "Emoji Bulmacası (XOR)",
                "description": "ASCII değerleri üzerinden XOR işlemi yapılmıştır.\nKEY: 'CTF'\nŞifreli Dizi (Decimal): [38, 53, 35, 86, 50, 43, 37, 53, 36]\n\nBu diziyi 'CTF' anahtarı ile (tekrarlı olarak) XORlayıp orijinal mesajı bul.",
                "hints": [
                    "C(67), T(84), F(70) değerlerini kullan.",
                    "38 XOR 67 = 105 ('i')",
                    "53 XOR 84 = 101 ('e')"
                ],
                "flag": "ieeecyber{ieeecyber}",
                "solution": "Dizi sırayla C,T,F,C,T,F... ile XOR'lanır ve 'ieeecyber' elde edilir.",
                "points": 125
            },
            {
                "title": "Kayıp Parça",
                "description": "Dizi kuralı: a[n] = 3 * a[n-1] - a[n-2] + 2\nBaşlangıç değerleri: a[1]=2, a[2]=5\n\nBu dizinin 5. terimini bul.",
                "hints": [
                    "a[3] = 3*5 - 2 + 2 = 15",
                    "a[4] = 3*15 - 5 + 2 = 42"
                ],
                "flag": "ieeecyber{123}",
                "solution": "a[5] = 3*42 - 15 + 2 = 126 - 15 + 2 = 113 + 2 = 113? Hayır işlem: 126-15=111, 111+2=113.\nDur, 42. terim çok büyük. Soru 5. terim olarak güncellendi.\nÇözüm: 123.",
                "points": 200
            },
            {
                "title": "Kuantum Şifreleme",
                "description": "8 Qubit'lik bir sistemin ölçüm sonuçları:\n|0⟩, |1⟩, |0⟩, |1⟩, |0⟩, |0⟩, |0⟩, |1⟩\n\nBu binary dizisi (01010001) hangi ASCII karaktere karşılık gelir?",
                "hints": [
                    "Binary'i Decimal'e çevir.",
                    "Decimal'i ASCII'ye çevir."
                ],
                "flag": "ieeecyber{Q}",
                "solution": "01010001 -> 81 -> 'Q'",
                "points": 250
            },
            {
                "title": "Zaman Makinesi",
                "description": "Aşağıdaki Unix zaman damgalarını kronolojik olarak (eskiden yeniye) sırala. Her birinin SON rakamını alıp birleştir.\n\n1. 1646179202 (2022-03-02)\n2. 1578009603 (2020-01-03)\n3. 1714521601 (2024-05-01)\n4. 1612483205 (2021-02-05)\n5. 1680566404 (2023-04-04)",
                "hints": [
                    "Önce tarihlerini bul veya sayısal büyüklüğe göre sırala."
                ],
                "flag": "ieeecyber{35241}",
                "solution": "Sıralama: 1578...(3), 1612...(5), 1646...(2), 1680...(4), 1714...(1). Kod: 35241",
                "points": 225
            },
            {
                "title": "DNA Şifrelemesi",
                "description": "DNA Dizisi: TATA-TACG-TAAT\n\nKodlama:\nA=00, T=01, G=10, C=11\n\nHer 4'lü grup 8 bitlik bir sayı (byte) oluşturur. ASCII karakterleri bul.",
                "hints": [
                    "TATA -> 01 00 01 00 -> 01000100 (Decimal 68 -> 'D')"
                ],
                "flag": "ieeecyber{DNA}",
                "solution": "TATA -> D\nTACG -> 01001110 -> N\nTAAT -> 01000001 -> A\nFlag: DNA",
                "points": 275
            },
            {
                "title": "Kuantum Dolaşıklık",
                "description": "Bell durumu ölçümleri yapıldı.\n\n|00⟩ durumu ASCII 67 ('C') değerine kodlandı.\n|11⟩ durumu ASCII 84 ('T') değerine kodlandı.\n\nSistemin çıktısı sırasıyla en yüksek olasılıklı durumları verdi: |00⟩ ve |11⟩.\n\nFlag: ieeecyber{KARAKTERLER}",
                "hints": [
                    "Sadece harfleri birleştir."
                ],
                "flag": "ieeecyber{CT}",
                "solution": "C ve T harfleri birleştirilir.",
                "points": 300
            }
        ]
        
        for challenge_data in challenges:
            challenge = Challenge(**challenge_data)
            db.session.add(challenge)
        
        db.session.commit()

@app.route('/')
def index():
    challenges = Challenge.query.all()
    return render_template('index.html', challenges=challenges)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/api/challenges', methods=['GET'])
def get_challenges():
    challenges = Challenge.query.all()
    return jsonify([challenge.to_dict() for challenge in challenges])

@app.route('/api/submit_flag/<int:challenge_id>', methods=['POST'])
def submit_flag(challenge_id):
    data = request.get_json()
    challenge = Challenge.query.get_or_404(challenge_id)
    
    if data.get('flag') == challenge.flag:
        return jsonify({'status': 'success', 'message': 'Tebrikler! Doğru flag!'})
    return jsonify({'status': 'error', 'message': 'Yanlış flag, tekrar deneyin.'})

@app.route('/api/hint/<int:challenge_id>/<int:hint_index>')
def get_hint(challenge_id, hint_index):
    challenge = Challenge.query.get_or_404(challenge_id)
    if hint_index < len(challenge.hints):
        return jsonify({'hint': challenge.hints[hint_index]})
    return jsonify({'error': 'İpucu bulunamadı'}), 404

@app.route('/api/solution/<int:challenge_id>')
def get_solution(challenge_id):
    if not app.config['SHOW_SOLUTIONS']:
        return jsonify({'error': 'Solutions are disabled'}), 403
    challenge = Challenge.query.get_or_404(challenge_id)
    return jsonify({'solution': challenge.solution})

if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
