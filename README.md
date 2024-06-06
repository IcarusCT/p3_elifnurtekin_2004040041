# p3_elifnurtekin_2004040041


# Duygusal Durumları Sınıflandırma Projesi | Elifnur Tekin | 2004040041

## Proje Tanımı
Bu proje, Türkçe yazılı metinlerden duygusal durumları sınıflandırmak için geliştirilmiş bir model içerir. 
Model, kullanıcıların yazdığı metinleri analiz ederek duygusal durumlarını tahmin eder.

ONEMLI : Model yuksek boyutta oldugundan drive yuklemesi yaptim lutfen projeyi calistirmadan once model dosyasini verilen drive linki uzerinden yukleyiniz.
(https://drive.google.com/file/d/1b4Ys82_xKW6cMAH4_CySUwNYH64SwAzk/view?usp=sharing)

## Dosyalar
app.py - Web arayüzüne bu dosyadan ulaşılabilir. 
dataset_generator.py - Sentetik data üretimi için yazılan kodun dosyası. 
testdata.csv - Dataset dosyası. 
training_model.ipynb - Model eğitim dosyası. 


## Platform
Bu proje Visual Studio Code üzerinde yazılmıştır. Model eğitimi için Google Colab kullanılmıştır. Sentetik veri oluşturma için OpenAI API kullanılmıştır.

## Kurulum Adımları
1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install flask zeyrek nltk joblib tensorflow
   ```
2. Uygulamayı başlatın:
   ```bash
   python app.py
   ```

## Kullanım Kılavuzu
Uygulama, `http://127.0.0.1:5000/` adresinde çalışacaktır. 
Kullanıcı bu adrese giderek metin girebilir ve duygusal sınıflandırma sonuçlarını görebilir.

## Veri Seti ve Ön İşleme Bilgileri
Proje, kullanıcılardan toplanan ve çeşitli duyguları ifade eden cümleleri içeren bir veri seti kullanır. 
Metinler, Zeyrek kütüphanesi kullanılarak kelimelere ve eklerine ayrılır. Bu adım modelin doğruluk oranının yükselmesi için eklenmiştir.

## Model Eğitimi ve Değerlendirme
Model, TensorFlow/Keras kullanılarak eğitilmiştir. 
Eğitim ve değerlendirme adımları, `training_model.ipynb` dosyasında detaylandırılmıştır.

## Dağıtım Talimatları
Projeyi başka bir bilgisayara dağıtmak için, proje dosyalarını kopyalayın ve yukarıdaki kurulum adımlarını izleyin. 
Gerekli tüm kütüphanelerin yüklü olduğundan emin olun ve uygulamayı başlatın.

