from os.path import expanduser
from aip import AipOcr
import os
from PIL import Image



def ocr_img(imgname,debug=0):

    #################设置你的百度api参数##############
    APP_ID = "23658549"
    API_KEY = "hGU9Z8eM8TIiNxf4YTPV8kao"
    SECRET_KEY = "cAX3DqAlU05spmoWq4Q4IFmK1YxFTR4C"
    ###############################################
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    #name="17.jpg"
    image = get_file_content(imgname)
    #APP_ID = "23658549"
    #API_KEY = "hGU9Z8eM8TIiNxf4YTPV8kao"
    #SECRET_KEY = "cAX3DqAlU05spmoWq4Q4IFmK1YxFTR4C"
    client = AipOcr(APP_ID,API_KEY,SECRET_KEY)
    options={}
    text=client.general(image)
    listt=text['words_result']
    lens=len(listt)
    try:
        for i in range(0,lens):
            strr=str(listt[i]).replace("{","").replace("}","")
            if(strr.find("个人参赛")!=-1 or strr.find("人参赛")!=-1):
                res=strr
                break
        res=res.replace("'","").replace(",","").replace(" ","")
        if(debug==1):
            print("定位到的信息:")
            print(res)           
        mark=res.find("top")
        mark1=res.find("left")
        mark2=res.find("width")
        mark3=res.find("height")
        h=int(res[mark3+7:])*3
        w=int(res[mark2+6:mark3])*3
        x=int(res[mark1+5:mark2])-w/3
        y=int(res[mark+4:mark1])+(h/3)
        #w=433
        #h=99
    except NameError:
        for i in range(0,lens):
            strr=str(listt[i]).replace("{","").replace("}","")
            if(strr.find("个人积分")!=-1 or strr.find("人积分")!=-1):
                res=strr
                break
        res=res.replace("'","").replace(",","").replace(" ","")
        if(debug==1):
            print("定位到的信息:")
            print(res)
        mark=res.find("top")
        mark1=res.find("left")
        mark2=res.find("width")
        mark3=res.find("height")
        h=int(res[mark3+7:])*3
        w=int(res[mark2+6:mark3])*3
        x=int(res[mark1+5:mark2])-w/3
        y=int(res[mark+4:mark1])+(h/3)
    im=Image.open(imgname)
    region=im.crop((x,y,x+w,y+h))
    region.save("./res1.png")
    region1=im.crop((x+w,y,x+w+w,y+h))
    region1.save("./res2.png")
    import pytesseract
    img=get_file_content('res1.png')
    img1=get_file_content('res2.png')
    tex=client.basicGeneral(img)
    tex1=client.basicGeneral(img1)
    listt2=tex['words_result']
    listt3=tex1['words_result']
    if(debug==1):
        print("baidu扫描res1.png结果:")
        print(listt2)
        print("baidu扫描res2.png结果:")
        print(listt3)
    try:
        strr2=str(listt2[0]).replace("'words':","").replace("{","").replace("}","").replace(" ","").replace("'","")
        strr3=str(listt3[0]).replace("'words':","").replace("{","").replace("}","").replace(" ","").replace("'","")
        num=int(strr2)
        score=int(strr3)
        res={}
        res['个人参赛次数']=num
        res['个人积分']=score
        res['err_code']=0
        return res
    except IndexError:
        BASE_DIR = os.path.dirname(__file__)
        zh_img = os.path.join(BASE_DIR, "res1.png")
        zh_img1 = os.path.join(BASE_DIR, "res2.png")
        zh = pytesseract.image_to_string(Image.open(zh_img), lang="eng")
        zh1 = pytesseract.image_to_string(Image.open(zh_img1), lang="eng")
        if(debug==1):
            print("tesseract扫描res1.png结果:")
            print(zh)
            print("tesseract扫描res2.png结果:")
            print(zh1)
        if(listt2==[] and str(zh).replace(" ","")!="" and listt3!=[]):
            num=int(zh)
            strr3=str(listt3[0]).replace("'words':","").replace("{","").replace("}","").replace(" ","").replace("'","")
            score=int(strr3)
            res={}
            res['err_code']=0
            res['个人参赛次数']=num
            res['个人积分']=score
            return res
        elif(listt2!=[] and str(zh1).replace(" ","")=="" and listt3==[]):
            strr2=str(listt2[0]).replace("'words':","").replace("{","").replace("}","").replace(" ","").replace("'","")
            num=int(strr2)
            score=int(zh1)
            res={}
            res['err_code']=0
            res['个人参赛次数']=num
            res['个人积分']=score
            return res
        else:
            res={}
            res['err_code']=1
            res['个人参赛次数']="error"
            res['个人积分']="error"
            return res
    except ValueError:
        res={}
        res['err_code']=1
        res['个人参赛次数']="error"
        res['个人积分']="error"
        res['reason']="可能是字体原因"
        return res
