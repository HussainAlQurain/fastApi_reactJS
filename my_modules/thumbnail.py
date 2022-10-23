import requests, bs4, re

pattern = re.compile(r'(http)(\S+)(.)(jpg|jpeg|png|webp)')

def find_img(url):
    links = []
    results = requests.get(url)
    soup = bs4.BeautifulSoup(results.text, 'lxml')
    selected = soup.select('link')
    selected2 = soup.select('meta')
    tmp = re.findall(pattern, str(selected))
    tmp2 = re.findall(pattern, str(selected2))

    for link in tmp:
        st = link[0] + link[1] + link[2] + link[3]
        links.append(st)
    for link in tmp2:
        st = link[0] + link[1] + link[2] + link[3]
        links.append(st)

    for x in links:
        if 'maxres' in x:
            return x
    return links[-1]



if __name__ == "__main__":
    print(find_img('https://www.youtube.com/watch?v=7t2alSnE2-I'))
