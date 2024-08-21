
# chrome_driver_path = ChromeDriverManager().install()
# browser_service = Service(executable_path=chrome_driver_path)
# options = Options()
# # options.add_argument('--headless')
# # options.add_argument('--no-sandbox')
# options.add_argument("--window-size=1200,600")
# options.add_argument('--disable-dev-shm-usage')
# browser = Chrome(service=browser_service, options=options)

# res = avto_alyans({})
# pprint(res)
# res_name = []
# with open('../autolist.txt', 'r', encoding='utf-8') as f:
#     lst = f.readlines()
#     for item in lst:
#         title = item.split('|')[0].strip()
#         res_name.append(title)
# for i in res:
#     if i[0] not in res_name:
#         print(i)