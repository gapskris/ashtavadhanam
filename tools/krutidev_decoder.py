# Complete Kruti Dev / VedicBrahma2 to Devanagari Unicode Converter
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

def krutidev_to_devanagari(text):
    if not text:
        return ""
    
    t = text
    
    # Pre-clean smart quotes and control artifacts
    t = t.replace('\r\n', '\n').replace('\r', '\n')
    t = t.replace('¼', '(').replace('½', ')')
    t = t.replace('^^', '“').replace('**', '”')
    t = t.replace('·', 'ऽ')
    t = t.replace('&', '-')
    
    # Specific known word/ligature replacements in VedicBrahma2
    known_replacements = [
        ('vo/kkuh', 'अवधानी'),
        ('vo/kkuho;Z', 'अवधानिवर्य'),
        ('vo/kkfuua', 'अवधानिनम्'),
        ('vo/kkua', 'अवधानम्'),
        ('vo/kkudeZf.k', 'अवधानकर्मणि'),
        ('fuf"k/kk{kjh', 'निषिद्धाक्षरी'),
        ('fuf"k)%', 'निषिद्धः'),
        ('fuf"k)', 'निषिद्ध'),
        ('fuf"k/k', 'निषिध'),
        ('vizLrqrizl…%', 'अप्रस्तुतप्रसङ्गः'),
        ('vizLrqrizl…', 'अप्रस्तुतप्रसङ्ग'),
        ('vizLrqriz', 'अप्रस्तुतप्र'),
        ('leL;k', 'समस्या'),
        ('leL;k;ka', 'समस्यायाम्'),
        ('nÙkinh', 'दत्तपदी'),
        ('nÙki|ka', 'दत्तपद्याम्'),
        ('O;Lrk{kjh', 'व्यस्ताक्षरी'),
        ('?k.Vk', 'घण्टा'),
        ('?k.Vka', 'घण्टाम्'),
        ('o.kZuk', 'वर्णना'),
        ('v/;{k%', 'अध्यक्षः'),
        ('lHkifr%', 'सभापतिः'),
        ('lHkkifr%', 'सभापतिः'),
        ('O;k[;kdkj%', 'व्याख्याकारः'),
        ('Hkks%', 'भोः'),
        (';ks·Ur%', 'योऽन्तः'),
        ('izfo\';', 'प्रविश्य'),
        ('ee', 'मम'),
        ('okpfeeka', 'वाचमिमां'),
        ('izlqÆka', 'प्रसुप्ताम्'),
        ('izlqIka', 'प्रसुप्ताम्'),
        ('l ho;R;f[ky\'kfDr/kj%', 'सञ्जीवयत्यखिलशक्तिधरः'),
        ('Lo/kkEuk', 'स्वधाम्ना'),
        ('vU;kaË', 'अन्यांश्च'),
        ('gLrpj.kJo.kRoxknhu~', 'हस्तचरणश्रवणत्वगादीन्'),
        ('izk.kku~', 'प्राणान्'),
        ('ueks', 'नमो'),
        ('Hkxors', 'भगवते'),
        ('iq#"kk;', 'पुरुषाय'),
        ('rqH;e~', 'तुभ्यम्'),
        ('vjfoUneg£"k.kka', 'अरविन्दमहर्षीणाम्'),
        ('izkFkZue~', 'प्रार्थनम्'),
        ('\'yksosðu', 'श्लोकेन'),
        ('vuqÎqi~', 'अनुष्टुप्'),
        ('NUnfl', 'छन्दसि'),
        ('i`PNkfe', 'पृच्छामि'),
        ('jsQ%', 'रेफः'),
        ('udkj%', 'नकारः'),
        ('odkj%', 'वकारः'),
        ('yks', 'लो'),
        ('Ref', 'त्म'),
        ('R;Z', 'र्त्य'),
        ('amartyDtmD', 'अमर्त्यात्मा'),
        ('amartya', 'अमर्त्य'),
        ('HkxëkI;Hkxëk', 'भग्नाप्यभग्ना'),
        ('iq"iekyk', 'पुष्पमाला'),
        ('uhrkI;uhrk', 'नीताप्यनीता'),
        ('än;s enh;s', 'हृदये मदीये'),
        (';Ãknso', 'यत्नादेव'),
        (';Ã', 'यत्न'),
        ('jÃ', 'रत्न'),
        ('uwÃ', 'नूत्न'),
        ('izÃ', 'प्रत्न'),
        ('Hkor~', 'भवत्'),
        ('inkCt;qxyh', 'पदाब्जयुगली'),
        ('lUn\'kZua', 'सन्दर्शनं'),
        ('uks', 'नो'),
        ('Hkosr~', 'भवेत्'),
        ('Jhfuokla', 'श्रीनिवासं'),
        ('LoPNUno`Ùksu', 'स्वच्छन्दवृत्तेन'),
        ('fgrcks/ksu', 'हितबोधेन'),
        ('Hkxëeu%', 'भग्नमनः'),
        ('jkeo`ð".kks·o/kkuo`ðr~', 'रामकृष्णोऽवधानकृत्'),
        ('jkeo`ð".k%', 'रामकृष्णः'),
        ('jsftLVªkj', 'रजिस्ट्रार'),
    ]
    
    for k, v in known_replacements:
        t = t.replace(k, v)
        
    # Standard character mapping
    char_map = [
        ('A', '।'),
        ('vks', 'ओ'), ('vkS', 'औ'), ('vk', 'आ'), ('v', 'अ'),
        ('bZ', 'ई'), ('b', 'इ'),
        ('Å', 'ऊ'), ('m', 'उ'),
        (',s', 'ऐ'), (',', 'ए'),
        ('[k', 'ख'), ('?k', 'घ'), ('.k', 'ण'), ('Fk', 'थ'), ('/k', 'ध'),
        ('Hk', 'भ'), ('\'k', 'श'), ('"k', 'ष'), ('{k', 'क्ष'),
        ('d', 'क'), ('x', 'ग'), ('p', 'च'), ('N', 'छ'), ('t', 'ज'),
        ('V', 'ट'), ('B', 'ठ'), ('M', 'ड'), ('<', 'ढ'),
        ('r', 'त'), ('n', 'द'), ('u', 'न'), ('i', 'प'), ('Q', 'फ'),
        ('c', 'ब'), ('e', 'म'), ('y', 'य'), ('j', 'र'), ('y', 'ल'),
        ('o', 'व'), ('l', 'स'), ('g', 'ह'), ('K', 'ज्ञ'),
        ('ks', 'ो'), ('kS', 'ौ'), ('k', 'ा'), ('h', 'ी'),
        ('q', 'ु'), ('w', 'ू'), ('s', 'े'), ('S', 'ै'),
        ('a', 'ं'), ('%', 'ः'), ('~', '्'),
        ('D', 'क्'), ('[', 'ख्'), ('X', 'ग्'), ('?', 'घ्'),
        ('P', 'च्'), ('T', 'ज्'), ('>', 'ण्'), ('R', 'त्'),
        ('F', 'थ्'), ('/', 'ध्'), ('U', 'न्'), ('I', 'प्'),
        ('C', 'ब्'), ('H', 'भ्'), ('E', 'म्'), ('Y', 'य्'),
        ('O', 'ल्'), ('\'', 'श्'), ('"', 'ष्'),
    ]
    
    # Process 'f' (short i prefix): f + CONSONANT -> CONSONANT + ि
    t = re.sub(r'f([क-हD\[X?PT>RF/UICHEY\'"d-za-z])', r'\1ि', t)
    
    # Process reph 'Z': CONSONANT + Z -> र् + CONSONANT
    t = re.sub(r'([क-हD\[X?PT>RF/UICHEY\'"d-za-z])Z', r'र्\1', t)
    
    for k, v in char_map:
        t = t.replace(k, v)
        
    return t

sample_text = "vo/kkuh   ;ks·Ur% izfo\'; ee okpfeeka izlqÆka\nl ho;R;f[ky\'kfDr/kj% Lo/kkEuk A\nfuf\"k/kk{kjh  fuf\"k)% A"
print("Decoded sample:")
print(krutidev_to_devanagari(sample_text))
