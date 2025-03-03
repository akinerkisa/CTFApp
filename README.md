# CTFApp

## Kurulum

1. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı başlatın:
```bash
python app.py
```

3. Tarayıcınızda şu adresi açın:
```
http://localhost:5000
```


### Güvenlik Ayarları
- Bu uygulama localde çalıştırılmak üzere yapılmıştır. Ancak local dışında kullanmak için şu önerileri izleyebilirsiniz:
- Debug modunu kapatmak için `app.run(debug=False)` yapın
- `SECRET_KEY`'i değiştirin
- İsterseniz çözüm endpoint'ini kaldırın

## Güvenlik
- Bu uygulama eğitim amaçlıdır
- Prod ortamında kullanmadan önce güvenlik önlemlerini alın
- Varsayılan olarak çözümler görünür durumdadır, isterseniz kaldırabilirsiniz

## SSS
### Yeni Soru Ekleme
`app.py` dosyasındaki `challenges` listesine yeni sorular ekleyebilirsiniz. Soru formatı:

```python
{
    "title": "Soru Başlığı",
    "description": "Soru açıklaması",
    "hints": ["İpucu 1", "İpucu 2"],
    "flag": "ieeecyber{flag}",
    "solution": "Çözüm açıklaması",
    "points": 100
}
```

### Soruları değiştirmek istiyorum
`app.py` içindeki `challenges` listesini düzenleyebilirsiniz.

### Çözümleri gizlemek istiyorum
`app.py`'den `/api/solution` endpoint'ini kaldırın veya şu şekilde koruma ekleyin:
```python
@app.route('/api/solution/<int:challenge_id>')
def get_solution(challenge_id):
    if not os.getenv('SHOW_SOLUTIONS', 'False').lower() == 'true':
        return jsonify({'error': 'Solutions are disabled'}), 403
    challenge = Challenge.query.get_or_404(challenge_id)
    return jsonify({'solution': challenge.solution})
``` 