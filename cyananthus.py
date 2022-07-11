from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def get_cvh_by_uid(uid, driver_path, options):
    new_url = "https://www.cvh.ac.cn/spms/detail.php?id=" + uid
    driver = webdriver.Chrome(executable_path=driver_path,options=options)
    driver.get(new_url)
    timeout = 30
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, 'reproductiveCondition')))
    except TimeoutException:
        print('Timed out waiting for' + url + ' to load')
        driver.quit()
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    tables = soup.find_all('table')
    new_list = list()
    # only get info from table for 鉴定信息 and 采集信息
    for table in tables:
        if any(item in table.get_text() for item in ['学名','中文名','采集人','采集时间']):
            rows = table.find_all('tr')
            for tr in rows:
                td = tr.find_all('td')
                row = [i.text for i in td]
                if row != []: # not empty
                    new_list.append(row)
    driver.close()
    new_dic = {d[0]:d[1] for d in new_list}
    return new_dic


def get_table_by_url(url, driver_path, options, get_rec_num = False):
    driver = webdriver.Chrome(executable_path=driver_path,options=options)
    driver.get(url)

    timeout = 30
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, 'spms_list')))
    except TimeoutException:
        driver.quit()
    if get_rec_num == True:
        rec_num = driver.find_element(By.ID,"total").text
    rows = driver.find_elements(By.XPATH,"//*[@data-collection-id]")
    out_lines = []
    for row in rows:
        uid = row.get_attribute('data-collection-id')
        new_dic = get_cvh_by_uid(uid,driver_path,options)
        value_list = [new_dic[x] for x in out_fields]
        out_line = '\t'.join(value_list)
        out_lines.append(out_line)
    driver.close()
    if get_rec_num == False:
        return out_lines
    else:
        return out_lines, rec_num

Usage = "%prog [options] taxa driver_path"
version = '%prog 20210328.1'

# this assumes the mpileip file is only from one contig so no dictionary is needed
taxa = sys.argv[1]
driver_path = sys.argv[2]
out_fields = ['中文名','采集人','采集时间','采集地','生境','海拔','习性','物候期']
options = Options()
options.headless = True

def main():
    with open(taxa + '_cvh.csv', 'w') as fh:
        fh.write('\t'.join(out_fields) + '\n')
        url_0 = "https://www.cvh.ac.cn/spms/list.php?taxonName=" + taxa
        out_lines, rec_num = get_table_url(url_0, driver_path, options, get_rec_num = True)
        fh.write('\n'.join(out_lines) + '\n')
        for i in range(1,round(int(rec_num[1:-3])/30/30)):
            print(30*i)
            url = "https://www.cvh.ac.cn/spms/list.php?taxonName=" + taxa + '&offset=' + str(30*i)
            out_lines = get_table_by_url(url, driver_path, options)
            fh.write('\n'.join(out_lines) + '\n')

if __name__ == "__main__":
    main()
