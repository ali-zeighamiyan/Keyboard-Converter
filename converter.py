
import fasttext

fasttext.FastText.eprint = lambda x: None
model_fa = fasttext.load_model("/content/drive/MyDrive/NLP/persian-model.bin")
model_en = fasttext.load_model("/content/drive/MyDrive/NLP/english-model.bin")

fa_to_en = {'ض': 'q', 'ص': 'w', 'ث': 'e', 'ق': 'r', 'ف': 't', 'غ': 'y',
                     'ع': 'u', 'ه': 'i', 'خ': 'o', 'ح': 'p', 'ش': 'a', 'س': 's',
                     'ی': 'd', 'ب': 'f', 'ل': 'g', 'ا': 'h', 'ت': 'j', 'ن': 'k',
                     'م': 'l', 'ظ': 'z', 'ط': 'x', 'ز': 'c', 'ر': 'v', 'ذ': 'b',
                     'د': 'n', 'ئ': 'm', "ک":";", "گ":"'", "و":","}

en_to_fa = {"q":"ض", "w":"ص", "e":"ث", "r":"ق", "t":"ف", "y":"غ", "u":"ع",
             "i":"ه", "o":"خ", "p":"ح", "a":"ش", "s":"س", "d":"ی", "f":"ب",
             "g":"ل", "h":"ا", "j":"ت", "k":"ن", "l":"م", "z":"ظ", "x":"ط",
             "c":"ز", "v":"ر",  "b":"ذ", "n":"د", "m":"ئ", ";":"ک", "'":"گ",
             "[":"ج", "]":"چ", "\\":"پ", "C":"ژ", ",":"و"}

def detect_lang(word):
  weights = {"fa-W":0, "en-W":0}
  for txt in word:
    if txt in fa_to_en:
      weights["fa-W"] += 1
    elif txt in en_to_fa:
      weights["en-W"] += 1

  if weights["fa-W"] > weights["en-W"]:
    return "fa"
  else:
    return "en"

def get_text_pred(text, lang):
  if lang == "en":
    res = model_en.predict(text)

  elif lang == "fa":
    res = model_fa.predict(text)
  return res[0][0]

def convert_text(text, source, target):
  converted_text = ""
  if source == "en" and target == "fa":
    keyboard_ = en_to_fa
  elif source == "fa" and target == "en":
    keyboard_ = fa_to_en

  for letter in text:
        if letter in keyboard_:
          converted_text += keyboard_[letter]
        else:
          converted_text += letter
  return converted_text


def correct_text(user_input_text):
  lang = detect_lang(user_input_text)
  status = get_text_pred(user_input_text, lang)

  if status == "__label__invalid":
    if lang == "en":
      converted_lang = "fa"
      print("invalid english text!")
      converted_text = convert_text(user_input_text, source="en", target="fa")
      retrun_text = converted_text


    elif lang == "fa":
      converted_lang = "en"
      print("invalid persian text!")
      converted_text = convert_text(user_input_text, source="fa", target="en")
      retrun_text = converted_text
      
    if get_text_pred(converted_text, converted_lang) == "__label__invalid":
      print("tatally invalid text! ...  ")
      retrun_text = user_input_text

  else:
    print("valid text ...")
    retrun_text = user_input_text

  return retrun_text

user_input_text = input()

correct_text(user_input_text)
