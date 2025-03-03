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
                "description": "Bir yapay zeka modelinin eğitim loglarında ilginç bir pattern keşfettik. Model, her epoch'ta belirli bir hata oranı gösteriyor:\n\nEpoch 1: 0.8415\nEpoch 2: 0.9093\nEpoch 3: 0.1411\nEpoch 4: -0.7568\nEpoch 5: -0.9589\nEpoch 6: -0.2794\nEpoch 7: 0.6570\n\nBu sayılar aslında gizli bir mesaj içeriyor. Her sayı, -1 ile 1 arasında normalize edilmiş durumda.\n\nFlag'i bulmak için bu sayıları 0-255 aralığına dönüştürüp ASCII karakterlerine çevirmen gerekiyor.\n\nFormül: int(((x + 1) / 2) * 255)",
                "hints": [
                    "Bu sayılar sinüs fonksiyonuna benzer bir dalgalanma gösteriyor",
                    "Sayıları -1,1 aralığından 0,255 aralığına dönüştürmen gerekiyor",
                    "Python ile dönüşüm yapıp, chr() fonksiyonu ile karakterlere çevirebilirsin"
                ],
                "flag": "ieeecyber{sin}",
                "solution": "1. Her sayı için: int(((x + 1) / 2) * 255) formülü uygulanır\n2. Çıkan sayılar: 115, 105, 110 (ASCII)\n3. chr() ile karakterlere çevrilince: 'sin' elde edilir",
                "points": 150
            },
            {
                "title": "Görsel Şifreleme",
                "description": "Bir PNG dosyasının binary analizini yaparken, IDAT chunk'ında şüpheli bir pattern fark ettik. Her pixel değeri (R,G,B) şu şekilde:\n\n(73,69,69), (69,67,89), (66,69,82)\n\nBu RGB değerleri bir mesaj içeriyor olabilir mi?",
                "hints": [
                    "Her RGB üçlüsü bir kelime oluşturuyor",
                    "RGB değerleri ASCII karakter kodlarına karşılık geliyor",
                    "Değerleri karakterlere çevirip yanyana yazmalısın"
                ],
                "flag": "ieeecyber{IEE_ECY_BER}",
                "solution": "RGB değerleri ASCII'ye çevrilir:\n(73,69,69) -> 'IEE'\n(69,67,89) -> 'ECY'\n(66,69,82) -> 'BER'",
                "points": 125
            },
            {
                "title": "Fibonacci Şifrelemesi",
                "description": "Yeni bir şifreleme algoritması keşfettik. Algoritma, Fibonacci dizisini kullanarak metinleri şifreliyor.\n\nŞifrelenmiş mesaj:\n[377, 987, 987, 987, 2584, 6765, 377, 987, 1597]\n\nİpucu: Her sayı, Fibonacci dizisindeki konumuna karşılık gelen harfi temsil ediyor. Örneğin:\nF(1) = 1 -> A\nF(2) = 1 -> B\nF(3) = 2 -> C\nF(4) = 3 -> D\nF(5) = 5 -> E\n...",
                "hints": [
                    "Önce her sayının Fibonacci dizisindeki konumunu bulmalısın",
                    "Konumlar alfabedeki harflere karşılık geliyor",
                    "Python ile Fibonacci dizisi oluşturup index bulabilirsin"
                ],
                "flag": "ieeecyber{ieeecyber}",
                "solution": "1. Her sayının Fibonacci dizisindeki konumu bulunur\n2. 377->14, 987->16, 987->16, 987->16 ...\n3. Konumlar harflere çevrilir: 14->i, 16->e ...",
                "points": 175
            },
            {
                "title": "Polinom Bulmacası",
                "description": "Bir şifreleme sisteminde kullanılan özel bir polinom bulduk:\n\nP(x) = x³ - 15x² + 71x - 105\n\nBu polinomun üç kökü var ve bu kökler ASCII değerler olarak yorumlandığında anlamlı bir mesaj oluşturuyor.\n\nKökleri bulup, ASCII karakterlere çevirdiğinde flag'i elde edeceksin.",
                "hints": [
                    "Polinomun üç kökü var ve hepsi tam sayı",
                    "Kökler 65-90 aralığında (ASCII büyük harfler)",
                    "Python'da numpy.roots() fonksiyonunu kullanabilirsin"
                ],
                "flag": "ieeecyber{CTF}",
                "solution": "1. Polinomun kökleri: 67, 84, 70\n2. ASCII'ye çevrilince: C, T, F\n3. Flag: ieeecyber{CTF}",
                "points": 200
            },
            {
                "title": "Matris Operasyonları",
                "description": "Bir matris şifreleme sistemi keşfettik. Sistem şu matrisi kullanıyor:\n\n[2 1 3]\n[0 4 1]\n[1 2 3]\n\nBu matrisin determinantı, izi (trace) ve özdeğerlerinin (eigenvalues) toplamı sırasıyla flag'in üç parçasını oluşturuyor.\n\nHer sayıyı yan yana yazıp flag'i oluştur.",
                "hints": [
                    "Determinant: Matrisin determinantını hesapla",
                    "Trace: Köşegen elemanların toplamı",
                    "Özdeğerler: Karakteristik polinomun kökleri",
                    "Python'da numpy.linalg modülünü kullanabilirsin"
                ],
                "flag": "ieeecyber{197}",
                "solution": "1. Determinant = 19\n2. Trace (2+4+3) = 9\n3. Özdeğerlerin toplamı = 7\n4. Yanyana: 197",
                "points": 175
            },
            {
                "title": "Katmanlı Gizem",
                "description": "OSINT ekibimiz, şüpheli bir sunucuda aşağıdaki şifreli metni buldu:\n'fXJjZ2Zfdmd5aHp7ZXJvbHBycnJ2'\n\nEkip, şifreleme yönteminin üç farklı tekniğin art arda kullanılmasıyla oluşturulduğunu tespit etti.",
                "hints": [
                    "İlk katman: En yaygın base encoding yöntemi kullanılmış",
                    "İkinci katman: Sezar'ın en sevdiği şifreleme tekniği, ancak biraz modernize edilmiş",
                    "Son katman: Ayna ayna, söyle bana..."
                ],
                "flag": "ieeecyber{multi_step}",
                "solution": "1. Base64 decode\n2. ROT13 decode\n3. Ters çevirme işlemi",
                "points": 100
            },
            {
                "title": "Kriptografik Denklem",
                "description": "Gizli mesajlaşma sisteminde kullanılan bir şifreleme fonksiyonu keşfedildi:\n\nE(x) ≡ (19x + 7) mod 26\n\nSistemde şifrelenmiş mesaj olarak '0' değeri bulundu. Orijinal mesajı bulabilir misin?\n\nNot: Çözümü flag formatında gönder: ieeecyber{X} (X yerine bulduğun harfi yaz)",
                "hints": [
                    "Modüler aritmetikte çarpımsal ters kullanmalısın",
                    "19'un mod 26'da çarpımsal tersi 11'dir",
                    "Sonucu 0-25 arası sayıdan harfe çevirirken A=0, B=1, ... kullan"
                ],
                "flag": "ieeecyber{B}",
                "solution": "1. 0 ≡ 19x + 7 (mod 26)\n2. -7 ≡ 19x (mod 26)\n3. 19 ≡ 19x (mod 26)\n4. x ≡ 19 * 11 (mod 26) ≡ 1 (mod 26)\n5. 1 → B",
                "points": 150
            },
            {
                "title": "Regex Pattern Dedektifi",
                "description": "Güvenlik ekibimiz, sistemde şüpheli aktiviteler tespit etti. Web Application Firewall (WAF) loglarında çeşitli pattern eşleşmeleri, format hataları ve validasyon sonuçları görülüyor.\n\nBu loglar arasında, saldırganın bıraktığı özel formatta (ieeecyber{...}) bir mesaj olduğunu düşünüyoruz.\n\nGörevin, verilen log dosyasını inceleyerek doğru pattern'i kullanıp gizli mesajı bulmak.\n\nLog dosyası: <a href='/static/suspicious.log' target='_blank' class='text-blue-500 hover:text-blue-700 underline'>suspicious.log</a>",
                "hints": [
                    "Log dosyasında email formatları, URL pattern'leri ve özel formatlar var",
                    "Regex ile 'ieeecyber{' ile başlayıp '}' ile biten pattern'i yakala",
                    "Pattern: ^ieeecyber\\{([^}]+)\\}$"
                ],
                "flag": "ieeecyber{regex_1_flag}",
                "solution": "Log dosyasında regex pattern ^ieeecyber\\{([^}]+)\\}$ kullanılarak flag bulunur.\n\nRegex açıklaması:\n- ^ : Satır başı\n- ieeecyber\\{ : Tam olarak bu metni ara\n- [^}]+ : '}' karakteri dışındaki herhangi bir karakterden bir veya daha fazla tekrar\n- \\} : '}' karakteri ile bitir\n- $ : Satır sonu",
                "points": 75
            },
            {
                "title": "Askeri Haberleşme",
                "description": "II. Dünya Savaşı'ndan kalma bir haberleşme cihazından alınan mesaj:\n\n'IJQXGZJTGI======'\n\nNot: Mesajı çözdükten sonra ieeecyber{mesaj} formatında gönder.",
                "hints": [
                    "Bu kodlama yöntemi, 32 farklı karakter kullanır",
                    "Eşittir işaretleri kodlamanın sonunda padding olarak kullanılır"
                ],
                "flag": "ieeecyber{Base32}",
                "solution": "Base32 decode işlemi yapılarak çözülür",
                "points": 50
            },
            {
                "title": "Zaman Kapsülü",
                "description": "Bir zaman kapsülü bulduk. Üzerinde sadece şu sayı yazıyor:\n\n1704067200\n\nBu sayının anlamını çözüp, tarihi ieeecyber{YYYY-MM-DD} formatında gönder.",
                "hints": [
                    "Bu sayı, 1 Ocak 1970'den itibaren geçen süreyi temsil ediyor",
                    "Süre birimi olarak saniye kullanılmış"
                ],
                "flag": "ieeecyber{2024-01-01}",
                "solution": "Unix timestamp'i datetime'a çevrilerek çözülür",
                "points": 50
            },
            {
                "title": "Ayna Yazısı",
                "description": "Bir siber saldırı sonrası sistemde kalan tek ipucu, bu garip formattaki metin:\n\n'}pets_iltum{rebycee i'\n\nNot: Metni doğru formata getirdiğinde anlamlı bir flag elde edeceksin.",
                "hints": [
                    "Metni farklı bir perspektiften okumayı dene",
                    "Ayna görüntüsü gibi düşün"
                ],
                "flag": "ieeecyber{multi_step}",
                "solution": "Metin karakterleri ters sırada yazılarak çözülür",
                "points": 25
            },
            {
                "title": "Hexadecimal Bulmaca",
                "description": "Bir binary dosyanın hex dump çıktısında şüpheli bir dizi bulundu:\n\n6965656563796265727b6865785f666c61677d\n\nBu hex değerinin arkasında ne gizleniyor?",
                "hints": [
                    "Her iki hex karakter bir ASCII değerini temsil eder",
                    "Hex to ASCII çevirici kullanabilirsin"
                ],
                "flag": "ieeecyber{hex_flag}",
                "solution": "Hex to ASCII dönüşümü yapılarak çözülür",
                "points": 75
            },
            {
                "title": "Gürültülü Sinyal",
                "description": "Bozuk bir iletişim kanalından alınan mesaj parazitlerle dolu:\n\n'i2e3e4e5c6y7b8e9r{b1a2s3e4_5m6o7d8u9l0e}'\n\nParazitleri temizleyip orijinal mesajı bulabilir misin?",
                "hints": [
                    "Parazitler sayısal karakterler olarak eklenmiş",
                    "Temiz sinyal sadece harflerden oluşuyor"
                ],
                "flag": "ieeecyber{base_module}",
                "solution": "Metindeki tüm rakamlar silinerek çözülür",
                "points": 50
            },
            {
                "title": "Çift Katmanlı Encoding",
                "description": "Güvenli iletişim için iki farklı encoding yöntemi art arda kullanılmış:\n\n'cWhueV9yYXBicXI='\n\nNot: İlk yöntem en popüler base encoding, ikincisi ise uğursuz sayı.",
                "hints": [
                    "İlk katmanı çözmek için en yaygın base encoding yöntemini kullan",
                    "İkinci katman için ROT13 şifreleme tekniği kullanılmış",
                    "Sıralama önemli: Önce Base64, sonra ROT13"
                ],
                "flag": "ieeecyber{dual_encode}",
                "solution": "1. Base64 decode -> 'qhny_rapbqr'\n2. ROT13 decode -> 'dual_encode'\n3. Flag formatına çevir: ieeecyber{dual_encode}",
                "points": 125
            },
            {
                "title": "Sezar'ın Dijital Mesajı",
                "description": "Modern Sezar şifreleme tekniği kullanılarak kodlanmış mesaj:\n\n'qmmmkgjmz{shift8}'\n\nNot: Şifreleme algoritması klasik Sezar şifrelemesinin bir varyasyonunu kullanıyor.",
                "hints": [
                    "Klasik Sezar şifrelemesi yerine sabit bir kayma miktarı kullanılmış",
                    "Kayma miktarı flag içinde gizlenmiş olabilir"
                ],
                "flag": "ieeecyber{shift8}",
                "solution": "Her harf alfabede 8 pozisyon geri kaydırılarak çözülür",
                "points": 100
            },
            {
                "title": "Gizli Harf",
                "description": "Bir metin dosyasında şifreli bir mesaj bulduk. Mesaj şu şekilde:\n\n'Gizli harf: 01001000'\n\nBu binary kodu çözerek gizli harfi bulabilir misin? Çözümü flag formatında gönder: ieeecyber{X} (X yerine bulduğun harfi yaz).",
                "hints": [
                    "Binary kod ASCII karakterleri temsil eder.",
                    "01001000, ASCII tablosunda bir harfe karşılık gelir."
                ],
                "flag": "ieeecyber{H}",
                "solution": "Binary kod ASCII'ye çevrilir: 01001000 -> H",
                "points": 50
            },
            {
                "title": "Sayıların Gizemi",
                "description": "Bir sistemde şu sayı dizisi bulundu:\n\n'105 101 101 101 99 121 98 101 114'\n\nBu sayıların gizemini çözerek flag'i bulabilir misin?",
                "hints": [
                    "Her sayı bir ASCII karakterini temsil eder.",
                    "Sayıları ASCII tablosuna çevirerek gizli mesajı bulabilirsin."
                ],
                "flag": "ieeecyber{ieeecyber}",
                "solution": "Sayılar ASCII'ye çevrilir: 105 -> i, 101 -> e, ... -> ieeecyber",
                "points": 75
            },
            {
                "title": "Gizli QR Kod",
                "description": "Bir sistemde şifreli bir QR kod bulundu. QR kodu tarattığında şu metni elde ediyorsun:\n\n'ieeecyber{cXJfY29kZQ==}'\n\nAncak bu metin doğru flag değil. Doğru flag'i bulmak için bir işlem yapman gerekiyor.",
                "hints": [
                    "QR koddan çıkan metin Base64 ile encode edilmiş.",
                    "Decode işlemi yaparak doğru flag'i bulabilirsin."
                ],
                "flag": "ieeecyber{qr_code}",
                "solution": "Base64 decode işlemi yapılarak çözülür: 'cXJfY29kZQ==' -> 'qr_code'",
                "points": 100
            },
            {
                "title": "Sesli Mesaj",
                "description": "Bir saldırganın bıraktığı ses dosyasını analiz ettik. Ses dosyasını dinlediğimizde bir Morse kodu duyduk:\n\n'.... . .-.. .-.. --- / .-- --- .-. .-.. -..'\n\nBu mesajı çözerek flag'i bulabilir misin?",
                "hints": [
                    "Morse kodunda her harf bir dizi nokta ve çizgi ile temsil edilir.",
                    "Boşluklar harfler arasında, '/' ise kelimeler arasında kullanılır."
                ],
                "flag": "ieeecyber{HELLO_WORLD}",
                "solution": "Morse kodu çözülerek mesaj elde edilir: '.... . .-.. .-.. --- / .-- --- .-. .-.. -..' -> 'HELLO WORLD'",
                "points": 125
            },
            {
                "title": "Şifreli Günlük",
                "description": "Bir günlük dosyasında şu şifreli metni bulduk:\n\n'V2UgYXJlIGxlYXJuaW5nIGNyeXB0b2dyYXBoeSE='\n\nBu mesajı çözerek flag'i bulabilir misin?",
                "hints": [
                    "Mesaj Base64 ile encode edilmiş.",
                    "Decode işlemi yaparak gizli mesajı bulabilirsin."
                ],
                "flag": "ieeecyber{We_are_learning_cryptography!}",
                "solution": "Base64 decode işlemi yapılarak çözülür: 'V2UgYXJlIGxlYXJuaW5nIGNyeXB0b2dyYXBoeSE=' -> 'We are learning cryptography!'",
                "points": 100
            },
            {
                "title": "Gizli Koordinatlar",
                "description": "Bir sistemde şu koordinatlar bulundu:\n\n'41.0082, 28.9784'\n\nBu koordinatların hangi şehre ait olduğunu bul ve flag formatında gönder: ieeecyber{ŞEHİR_ADI}.",
                "hints": [
                    "Koordinatları bir harita servisi kullanarak kontrol edebilirsin.",
                    "Bu koordinatlar Türkiye'deki bir şehre ait."
                ],
                "flag": "ieeecyber{Istanbul}",
                "solution": "Koordinatlar haritada kontrol edilerek İstanbul olduğu bulunur.",
                "points": 75
            },
            {
                "title": "Gizli Şifreleme",
                "description": "Bir sistemde şu şifreli mesaj bulundu:\n\n'uryyb_jbeyq'\n\nBu mesajı çözerek flag'i bulabilir misin?",
                "hints": [
                    "Mesaj ROT13 şifreleme yöntemiyle şifrelenmiş.",
                    "ROT13, her harfi alfabede 13 pozisyon kaydırır."
                ],
                "flag": "ieeecyber{hello_world}",
                "solution": "ROT13 decode işlemi yapılarak çözülür: 'uryyb_jbeyq' -> 'hello_world'",
                "points": 100
            },
            {
                "title": "Gizli Dosya Adı",
                "description": "Bir sistemde şifreli bir dosya bulundu. Dosyanın adı: 'c2VjcmV0X2ZpbGUudHh0'.\n\nBu dosya adını çözerek flag'i bulabilir misin?",
                "hints": [
                    "Dosya adı Base64 ile encode edilmiş.",
                    "Decode işlemi yaparak doğru dosya adını bulabilirsin."
                ],
                "flag": "ieeecyber{secret_file}",
                "solution": "Base64 decode işlemi yapılarak çözülür: 'c2VjcmV0X2ZpbGUudHh0' -> 'secret_file.txt'",
                "points": 75
            },
            {
                "title": "Renklerin Dili",
                "description": "Bir web sitesinin kaynak kodunda ilginç bir CSS renk kodu dizisi bulduk:\n\n#69 #65 #65 #65 #63 #79 #62 #65 #72\n\nBu renk kodları bir mesaj içeriyor olabilir mi?",
                "hints": [
                    "Her renk kodu aslında bir sayıyı temsil ediyor",
                    "Hexadecimal sayıları başka bir formata çevirmeyi dene"
                ],
                "flag": "ieeecyber{ieeecyber}",
                "solution": "Hex renk kodları ASCII'ye çevrilir: 69 -> 'i', 65 -> 'e', vs.",
                "points": 100
            },
            {
                "title": "Emoji Bulmacası",
                "description": "Bir Discord sunucusunda şu emoji dizisini bulduk:\n\n🔒 + 🔑 = ❓\n\n🔒: 'gizli_mesaj'\n🔑: 'CTF2024'\n\nBu emojiler bir şifreleme algoritmasını temsil ediyor. 🔒 metni 🔑 ile şifreleniyor. Sonucu flag formatında gönder.",
                "hints": [
                    "Bu yaygın bir simetrik şifreleme yöntemi",
                    "Her karakter için XOR işlemi kullanılıyor",
                    "Python'da ord() ve chr() fonksiyonları işine yarayabilir"
                ],
                "flag": "ieeecyber{xor_crypto}",
                "solution": "Her karakter için XOR işlemi yapılır: ord('g') ^ ord('C'), ord('i') ^ ord('T'), vs.",
                "points": 125
            },
            {
                "title": "Kayıp Parça",
                "description": "Bir şifreleme algoritmasında kullanılan matematiksel bir dizi keşfettik. Dizinin ilk 10 terimi şöyle:\n\n[2, 5, 13, 35, 97, 275, 795, 2335, 6947, 20845]\n\nBu dizi özel bir kurala göre ilerliyor. Her terim bir önceki terimden belirli bir matematiksel işlemle elde ediliyor.\n\nDizinin 42. teriminin son üç basamağı flag'i oluşturuyor. Flag'i ieeecyber{XXX} formatında gönder (XXX yerine bulduğun 3 basamaklı sayıyı yaz).",
                "hints": [
                    "Her terim bir öncekiyle ilişkili: Örneğin 13 sayısı 5'ten nasıl elde edilmiş?",
                    "İşlem içinde çarpma ve toplama var",
                    "Her adımda sabit sayılar kullanılıyor",
                    "Python ile bir script yazarak çözebilirsin: a[n] = 3 * a[n-1] - a[n-2] + 2"
                ],
                "flag": "ieeecyber{947}",
                "solution": "1. Dizi şu kurala göre ilerliyor: a[n] = 3 * a[n-1] - a[n-2] + 2\n2. Her terim, bir önceki terimin 3 katından, iki önceki terim çıkarılıp 2 eklenerek elde ediliyor\n3. Python script ile 42. terime kadar hesaplanır\n4. 42. terim: 6,937,947\n5. Son üç basamak: 947",
                "points": 200
            },
            {
                "title": "Kuantum Şifreleme",
                "description": "Kuantum bilgisayar araştırma merkezinden sızan bir mesajı ele geçirdik. Mesaj şu şekilde:\n\n|ψ⟩ = |0⟩ + |1⟩ (H gate)\n|φ⟩ = |0⟩ - |1⟩ (X ve H gates)\n|θ⟩ = |1⟩ (X gate)\n|γ⟩ = |0⟩ (I gate)\n\nHer qubit durumu bir biti temsil ediyor. Qubit'lerin ölçüm sonuçlarını binary olarak yan yana yazıp, ASCII'ye çevirdiğinde anlamlı bir kelime elde edeceksin.\n\nNot: H gate süperpozisyon yaratır, X gate 0 ve 1'i değiştirir, I gate değişiklik yapmaz.",
                "hints": [
                    "Her qubit durumunu ölçtüğünde 0 veya 1 elde edersin",
                    "H gate sonrası ölçüm %50 ihtimalle 0 veya 1 verir, ama burada özel bir durum var",
                    "Qubit sıralaması önemli: ψ,φ,θ,γ",
                    "Elde ettiğin 4-bit değeri ASCII'ye çevirmelisin"
                ],
                "flag": "ieeecyber{QUBIT}",
                "solution": "1. |ψ⟩ ölçümü: 0 (süperpozisyon ama ilk bit)\n2. |φ⟩ ölçümü: 1 (süperpozisyon ama negatif)\n3. |θ⟩ ölçümü: 1 (X gate 0->1)\n4. |γ⟩ ölçümü: 0 (I gate değişiklik yok)\n5. Binary: 0110 -> ASCII'de 'Q'",
                "points": 250
            },
            {
                "title": "Zaman Makinesi",
                "description": "Gelecekten gelen bir mesaj bulduk. Mesaj, Unix timestamp'lerden oluşuyor ve her timestamp'in son rakamı özel bir anlam taşıyor:\n\n1751480531\n1814876542\n1907789523\n1635467894\n2024555435\n\nHer timestamp'in son rakamı, o tarihteki önemli bir olayın sırasını gösteriyor. Tarihleri kronolojik olarak sıralayıp, son rakamlarını birleştirdiğinde flag'i elde edeceksin.\n\nNot: Tarihleri yyyy-MM-dd formatında sıralaman gerekiyor.",
                "hints": [
                    "Önce timestamp'leri tarihe çevir",
                    "Tarihleri kronolojik olarak sırala",
                    "Son rakamları sırayla birleştir",
                    "Python'da datetime.fromtimestamp() kullanabilirsin"
                ],
                "flag": "ieeecyber{35241}",
                "solution": "1. Timestamp -> Tarih dönüşümü:\n1751480531 -> 2025-07-15\n1814876542 -> 2027-06-20\n1907789523 -> 2030-05-10\n1635467894 -> 2021-10-29\n2024555435 -> 2034-02-14\n2. Kronolojik sıralama:\n2021-10-29 (4)\n2025-07-15 (1)\n2027-06-20 (2)\n2030-05-10 (3)\n2034-02-14 (5)\n3. Son rakamlar: 35241",
                "points": 225
            },
            {
                "title": "DNA Şifrelemesi",
                "description": "Bir biyoteknoloji laboratuvarından sızan verilerde ilginç bir DNA dizisi bulduk:\n\nATGC-GCTA-TGCA-CGAT-AGCT\n\nBu DNA dizisi özel bir şifreleme sistemi kullanıyor:\n- Her 4'lü grup bir karakteri temsil ediyor\n- A=00, T=01, G=10, C=11 şeklinde binary temsil ediliyor\n- Her grup 8-bit binary oluşturuyor\n\nDNA dizisini çözüp, gizli mesajı bulabilir misin?",
                "hints": [
                    "Önce DNA bazlarını binary'e çevir",
                    "Her 4'lü grup 1 byte oluşturur",
                    "Binary'den ASCII'ye çevir",
                    "Örnek: ATGC -> 00011011"
                ],
                "flag": "ieeecyber{DNA}",
                "solution": "1. DNA -> Binary dönüşümü:\nATGC -> 00011011\nGCTA -> 10110100\nTGCA -> 01101100\nCGAT -> 11100001\nAGCT -> 00101101\n2. Binary -> ASCII:\n00011011 -> D\n10110100 -> N\n01101100 -> A",
                "points": 275
            },
            {
                "title": "Kuantum Dolaşıklık",
                "description": "İki kuantum parçacık arasındaki dolaşıklık (entanglement) durumunu gösteren bir ölçüm sonucu ele geçirdik:\n\n|ψ⟩ = (|00⟩ + |11⟩)/√2\n\nBu durumdan 1000 ölçüm yapıldı ve şu sonuçlar elde edildi:\n492: |00⟩\n508: |11⟩\n\nAyrıca, her ölçüm sonucunda özel bir sayaç değeri kaydedilmiş:\n|00⟩ -> 67 (C)\n|11⟩ -> 84 (T)\n\nBu bilgileri kullanarak gizli mesajı bulabilir misin?\n\nNot: Sayaç değerlerinin yanındaki harfler ipucu olabilir.",
                "hints": [
                    "Ölçüm sonuçlarının dağılımına dikkat et",
                    "Sayaç değerlerini ASCII olarak düşün",
                    "Kuantum dolaşıklıkta iki parçacık her zaman uyumlu davranır",
                    "Harfleri doğru sırada birleştirmelisin"
                ],
                "flag": "ieeecyber{QUANTUM_CT}",
                "solution": "1. Ölçüm dağılımı yaklaşık %50-%50 (kuantum dolaşıklık özelliği)\n2. |00⟩ durumu -> ASCII 67 -> 'C'\n3. |11⟩ durumu -> ASCII 84 -> 'T'\n4. Olasılık dağılımı ve ölçüm sonuçları 'QUANTUM' kelimesini işaret ediyor\n5. Final flag: QUANTUM_CT",
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