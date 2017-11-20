from urllib import request
import re
class Spider():
    url = "https://www.panda.tv/cate/lol"
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<span class="video-number">([\s\S]*?)</span>'

    def __getUrl(self):
        cont = request.urlopen(self.url)
        htmlCon = cont.read()
        html = str(htmlCon,encoding="utf-8")
        return html

    def __analysis(self,htmls):
        root_html = re.findall(self.root_pattern,htmls)
        # print(root_html[0])
        anchors = []
        for html in root_html:
            name = re.findall(self.name_pattern,html)
            number = re.findall(self.number_pattern,html)
            anchor = {'name':name,'number':number}
            anchors.append(anchor)
        return anchors
    #获取人数和姓名
    def __refine(self,anchors):
        for item in anchors:
            item['name'] = item['name'][0].strip()
        return anchors

    def __sort(self,anchors):
        anchors = sorted(anchors,key=self.__sort_seed,reverse=True)
        return anchors

    def __sort_seed(self,anchors):
        r = re.findall('\d*',anchors['number'][0])
        number = float(r[0])
        if '万' in anchors['number']:
            number = number * 10000
        return number

    def __show(self,anchors):
        for anchor in anchors:
            print("名字："+str(anchor['name'])+" 人数:"+str(anchor['number']))

    def getCont(self):
        htmls = self.__getUrl()
        anc = self.__analysis(htmls)
        anl = self.__refine(anc)
        anlnew = self.__sort(anl)
        self.__show(anlnew)


spi = Spider()
spi.getCont()
