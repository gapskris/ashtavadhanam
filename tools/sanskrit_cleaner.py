import re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

# Ensure krutidev_decoder is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from krutidev_decoder import krutidev_to_devanagari

def clean_sanskrit_text(text):
    if not text:
        return ""
    
    t = text
    # Strip any leading nulls, control chars, and Director chunk hex offsets
    t = re.sub(r'^[\x00-\x1f\s]+', '', t.strip())
    t = re.sub(r'^[0-9A-Fa-f\x00\s]+[,ए]?\s*', '', t)
    t = re.sub(r'0000[0-9A-Fa-f\x00\s]+[,ए]?\s*', '', t)
    t = re.sub(r'^[\x00-\x1f\s]+', '', t)
    
    # Specific known vocabulary and phrases in the Ashtavadhanam CD-ROM (raw Kruti Dev form)
    exact_phrases = [
        # Opening Vishnu/Aurobindo Stuti
        (';ks·Ur% izfo\'; ee okpfeeka izlqÆka', 'योऽन्तः प्रविश्य मम वाचमिमां प्रसुप्ताम्'),
        (';ks·Ur% izfo\'; ee okpfeeka izlqIka', 'योऽन्तः प्रविश्य मम वाचमिमां प्रसुप्ताम्'),
        (';ks·Ur%', 'योऽन्तः'),
        ('l\x8dho;R;f[ky\'kfDr/kj% Lo/kkEuk', 'सञ्जीवयत्यखिलशक्तिधरः स्वधाम्ना ।'),
        ('l ho;R;f[ky\'kfDr/kj% Lo/kkEuk', 'सञ्जीवयत्यखिलशक्तिधरः स्वधाम्ना ।'),
        ('vU;kaË gLrpj.kJo.kRoxknhu~', 'अन्यांश्च हस्तचरणश्रवणत्वगादीन्'),
        ('izk.kku~ ueks Hkxors iq#"kk; rqH;e~ AA', 'प्राणान् नमो भगवते पुरुषाय तुभ्यम् ॥'),
        ('izk.kku~ ueks Hkxors iq#"kk; rqH;e~', 'प्राणान् नमो भगवते पुरुषाय तुभ्यम्'),
        
        # Round 1 dialogues
        ('lEizfr vjfoUneg£"k.kka izkFkZue~ ,osðu \'yksosðu vuqÎqi~ NUnfl i`PNkfe A', 'सम्प्रति अरविन्दमहर्षीणां प्रार्थनम् एकेन श्लोकेन अनुष्टुप् छन्दसि पृच्छामि ।'),
        ('lEizfr vjfoUneg£"k.kka izkFkZue~', 'सम्प्रति अरविन्दमहर्षीणां प्रार्थनम्'),
        (',osðu \'yksosðu vuqÎqi~ NUnfl i`PNkfe', 'एकेन श्लोकेन अनुष्टुप् छन्दसि पृच्छामि'),
        ('jsQ% fuf"k)% A  j fuf"k)%', 'रेफः निषिद्धः । र निषिद्धः ।'),
        ('jsQ% fuf"k)% A j fuf"k)%', 'रेफः निषिद्धः । र निषिद्धः ।'),
        ('jsQ% fuf"k)% A', 'रेफः निषिद्धः ।'),
        ('j fuf"k)%', 'र निषिद्धः ।'),
        ('vo/kkuh  e', 'अवधानी: म'),
        ('vo/kkuh  v', 'अवधानी: अ'),
        
        # Aprastutaprasanga Round 1
        ('vo/kkuho;Z Hkor% bnkuha r=k dforkJko.kle;s ee ,d% lUnHkZ% Le`friFkekxPNr~ A', 'अवधानिवर्य ! भवतः इदानीं तत्र कविताश्रवणसमये मम एकः सन्दर्भः स्मृतिपथमागच्छत् ।'),
        ('\'kqæd%  ižizo`fÙkdHkk.ke~ vjp;r~ fdy \\', 'शूद्रकः पद्मप्राभृतकभाणम् अरचयत् किल ?'),
        ('\'kqæd%  ižizo`fÙkdHkk.ke~ vjp;r~ fdy', 'शूद्रकः पद्मप्राभृतकभाणम् अरचयत् किल ?'),
        ('rkjLorHkæ% bfr df\'pr~ Hkokn`\'k%', 'सारस्वतभद्रः इति कश्चित् भवादृशः'),
        ('lkjLorHkæ% bfr df\'pr~ Hkokn`\'k%', 'सारस्वतभद्रः इति कश्चित् भवादृशः'),
        ('l% ,oeso dforka oqðoZu~ inkfu vUos"k;f', 'सः एवमेव कवितां कुर्वन् पदानि अन्वेषयति'),
        ('rnk r=k uV% lekxR; i`PNfr&& ^^', 'तदा तत्र नटः समागत्य पृच्छति— “'),
        ('rnk r=k uV% lekxR; i`PNfr', 'तदा तत्र नटः समागत्य पृच्छति'),
        ('Hkks% iqjk.kinPNsnxzFkupeZdkj', 'भोः पुराणपदच्छेदग्रथनचर्मकार !'),
        ('¯d uÎxksiky bo uoinkfu vUos"kls \\**', 'किं नष्टगोपाल इव नवपदानि अन्वेषसे ?”'),
        ('¯d uÎxksiky bo uoinkfu vUos"kls', 'किं नष्टगोपाल इव नवपदानि अन्वेषसे ?'),
        ('¯d HkoUr% vfi rkn`\'kk% \\', 'किं भवन्तः अपि तादृशाः ?'),
        
        # Avadhani reply
        ('vga peZdkj% bR;=k izek.kefLr peZHkfýdk ee lehis vfLr A', 'अहं चर्मकारः इत्यत्र प्रमाणमस्ति, चर्मभस्त्रिका मम समीपे अस्ति ।'),
        (',oa eekfi vfLr ,oað peZ A vr% peZdkjRoa fl)e~ A', 'एवं ममापि अस्ति एवं चर्म, अतः चर्मकारत्वं सिद्धम् ।'),
        ('uo vUos"k.kefi drZqfePNkfe A uo uo inkUos"k.ke~ A uo uo HkkokUos"k.ke~ A', 'नव-अन्वेषणमपि कर्तुमिच्छामि, नव-नव-पदान्वेषणम्, नव-नव-भावान्वेषणम् ।'),
        (',rr~ fouk u lEHkofr ee fØ;k A', 'एतत् विना न सम्भवति मम क्रिया ।'),
        ('vr% Hkor% vuqxzgs.k vga ee peZdkjRoe~ v…hdjksfe A', 'अतः भवतः अनुग्रहेण अहं मम चर्मकारत्वम् अङ्गीकरोमि ।'),
        ('Hkoku~ peZdkjks u Hkofr peRdkjdkj% A', 'भवान् चर्मकारो न भवति, चमत्कारकारः !'),
        ('rnuUrja y fuf"k)% A y dkj%', 'तदनन्तरं ल निषिद्धः । लकारः निषिद्धः ।'),
        
        # Dialogues roles and cues
        ('vizLrqrizl\x85%', 'अप्रस्तुतप्रसङ्गः:'),
        ('vizLrqrizl…%', 'अप्रस्तुतप्रसङ्गः:'),
        ('vizLrqrizl…', 'अप्रस्तुतप्रसङ्ग:'),
        ('fuf"k/kk{kjh', 'निषिद्धाक्षरी:'),
        ('vo/kkuho;Z', 'अवधानिवर्य!'),
        ('vo/kkuh', 'अवधानी:'),
        ('leL;k', 'समस्या:'),
        ('nÙkinh', 'दत्तपदी:'),
        ('O;Lrk{kjh', 'व्यस्ताक्षरी:'),
        ('¼?k.Vk 1½', '🔔 (घण्टा १)'),
        ('¼?k.Vk 2½', '🔔 (घण्टा २)'),
        ('¼?k.Vk 3½', '🔔 (घण्टा ३)'),
        ('¼?k.Vk 4½', '🔔 (घण्टा ४)'),
        ('¼?k.Vk 5½', '🔔 (घण्टा ५)'),
        ('¼?k.Vk 6½', '🔔 (घण्टा ६)'),
        ('¼?k.Vk 7½', '🔔 (घण्टा ७)'),
        ('fdfŒr~ cysu rkM;rq ¼?k.Vka izfr½', 'किञ्चित् बलेन ताडयतु ! (घण्टां प्रति)'),
        ('udkj% fuf"k)%', 'नकारः निषिद्धः ।'),
        ('odkj% fuf"k)%', 'वकारः निषिद्धः ।'),
        ('oð oðdkj% fuf"k)%', 'वकारः निषिद्धः ।'),
        (',d% v{kj% nh;rke~', 'एकः अक्षरः दीयताम् ।'),
        ('vU;% ,d% v{kj% nh;rke~', 'अन्यः एकः अक्षरः दीयताम् ।'),
        ('amartyDtmDmartyalo\'nge', 'अमर्त्यात्मा मर्त्यलोऽङ्गे'),
        ('amartyDtmD', 'अमर्त्यात्मा'),
        ('HkxëkI;Hkxëk ee iq"iekyk', 'भग्नाप्यभग्ना मम पुष्पमाला'),
        ('HkxëkI;Hkxëk', 'भग्नाप्यभग्ना'),
        ('ee iq"iekyk', 'मम पुष्पमाला'),
        ('uhrkI;uhrk än;s enh;s', 'नीताप्यनीता हृदये मदीये'),
        ('uhrkI;uhrk', 'नीताप्यनीता'),
        ('än;s enh;s', 'हृदये मदीये'),
        (';Ãknso Hkor~ inkCt;qxyh lUn\'kZua uks Hkosr~', 'यत्नादेव भवत्पदाब्जयुगली सन्दर्शनं नो भवेत्'),
        (';Ãknso', 'यत्नादेव'),
        (';Ã', 'यत्न'),
        ('jÃ', 'रत्न'),
        ('uwÃ', 'नूत्न'),
        ('izÃ', 'प्रत्न'),
        ('lHkifr%', 'सभापतिः:'),
        ('lHkkifr%', 'सभापतिः:'),
        ('O;k[;kdkj%', 'व्याख्याकारः:'),
        ('fgrcks/ksu', 'हितबोधेन'),
        ('jkeo`ð".kks·o/kkuo`ðr~', 'रामकृष्णोऽवधानकृत्'),
        ('jkeo`ð".k%', 'रामकृष्णः'),
        ('jsftLVªkj', 'रजिस्ट्रार')
    ]
    
    for k, v in exact_phrases:
        t = t.replace(k, v)
        
    # Convert remainder from Kruti Dev to Devanagari
    t = krutidev_to_devanagari(t)
    
    # Post-clean Devanagari typewriter remnants
    t = t.replace('\\', '?')
    t = t.replace('^^', '“').replace('**', '”')
    t = t.replace('¯d', 'किं')
    t = t.replace('Lम`ति', 'स्मृति')
    t = t.replace('fÙk', 'त्ति')
    t = t.replace('पžप', 'पद्म')
    t = t.replace('z', '्र')
    t = t.replace('æ', 'द्र')
    t = t.replace('fdy', 'किल')
    t = t.replace('f\\', 'ति')
    t = t.replace(';Z', 'र्य')
    t = t.replace('t=k', 'तत्र')
    t = t.replace('T=k', 'तत्र')
    t = t.replace(';s', 'ये')
    t = t.replace(';f', 'ति')
    t = t.replace(';त्', 'यत्')
    t = t.replace(';े', 'ये')
    t = t.replace('Lम', 'स्म')
    t = t.replace('पzव`', 'प्रवृ')
    t = t.replace('स ीव;त्;ख्िायशक्ितधरः', 'सञ्जीवयत्यखिलशक्तिधरः')
    t = t.replace(';ोऽन्तः', 'योऽन्तः')
    t = t.replace('नष्िाधाक्षरी', 'निषिद्धाक्षरी:')
    t = t.replace('पžप्रव`fÙाकभाणम्', 'पद्मप्राभृतकभाणम्')
    t = t.replace('किय ?', 'किल ?')
    t = t.replace('त=ा', 'तत्र')
    t = t.replace('वुðर्वन्', 'कुर्वन्')
    t = t.replace('घ्', '?')
    t = t.replace('\x01', '')
    t = re.sub(r'^[0-9A-Fa-f\x00\s,ए]+', '', t)
    
    return t.strip()

if __name__ == '__main__':
    sample = "0000\x00118,vo/kkuh   ;ks·Ur% izfo'; ee okpfeeka izlqÆka\r            l\x8dho;R;f[ky'kfDr/kj% Lo/kkEuk A\r      vU;kaË gLrpj.kJo.kRoxknhu~\r      izk.kku~ ueks Hkxors iq#\"kk; rqH;e~ AA\r\rfuf\"k/kk{kjh  lEizfr vjfoUneg£\"k.kka izkFkZue~ ,osðu \'yksosðu vuqÎqi~ NUnfl i`PNkfe A\r\rvo/kkuh  v"
    print("Test clean Sanskrit:")
    print(clean_sanskrit_text(sample))
