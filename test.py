import requests
import json



# api_key = '5n1gh5mm940fmki7jm'
# id = 5349543151

# # url = f'https://TG-Lion.net?action=getNumber&apiKey={api_key}&YourID={id}&country_code=BD'
# # url = f'https://TG-Lion.net?action=getCode&number=+8801799438984&apiKey={api_key}&YourID={id}&logout_now=yes'
# # url = f'https://TG-Lion.net?action=logout_number&number=+8801799438984&apiKey={api_key}&YourID={id}'




# response = requests.get(url)
# print(response.json())



# {'name': 'بنغلاديش 🇧🇩', 'Number': '+8801799438984', 'price_buyer': '0.35', 'new_balance': 4.7, 'status': 'ok'}

# {'Number': '+8801799438984', 'code': None, 'pass': None, 'status': 'ok'}

# {'status': 'error', 'message': 'The number was not found in your account'}

# {'status': 'ok', 'message': 'Successfully logged out and deleted number +8801799438984'}

# {'Number': '+8801799438984', 'code': None, 'pass': None, 'status': 'ok'}

# {'status': 'error', 'cod': 201, 'message': 'Insufficient balance'}







# viotp







# url = 'https://api.viotp.com/users/balance?token=c9d209cce8994a3e909119899a142d00'
# url = 'https://api.viotp.com/networks/get?token=c9d209cce8994a3e909119899a142d00'
# url = 'https://api.viotp.com/service/getv2?token=c9d209cce8994a3e909119899a142d00&country=vn'

url = 'https://api.viotp.com/request/getv2?token=c9d209cce8994a3e909119899a142d00&serviceId=276&network=VINAPHONE'
# url = 'https://api.viotp.com/session/getv2?requestId=470364012&token=c9d209cce8994a3e909119899a142d00'

{'status_code': -2, 'message': 'Số dư quý khách không đủ !', 'success': False}

# response = requests.get(url)
# print(response.json())

# {'status_code': 200, 'message': 'Tạo yêu cầu thành công !', 'success': True, 'data': {'phone_number': '813042280', 're_phone_number': '0813042280', 'countryISO': 'VN', 'countryCode': '84', 'request_id': 470360613, 'balance': 19500}}


# {'status_code': 200, 'message': 'successful', 'success': True, 'data': {'ID': 470360613, 'ServiceID': 7, 'ServiceName': 'Facebook', 'Price': 1200, 'SmsContent': None, 'Status': 0, 'CreatedTime': '2025-05-10T21:58:10.517', 'IsSound': False, 'Code': None, 'PhoneOriginal': '0813042280', 'Phone': '813042280', 'CountryISO': 'VN', 'CountryCode': '84'}}

# {'status_code': 200, 'message': 'Tạo yêu cầu thành công !', 'success': True, 'data': {'phone_number': '947546984', 're_phone_number': '0947546984', 'countryISO': 'VN', 'countryCode': '84', 'request_id': 470362368, 'balance': 16800}}

# {'status_code': 200, 'message': 'successful', 'success': True, 'data': [{'id': 1, 'name': 'MOBIFONE'}, {'id': 2, 'name': 'VINAPHONE'}, {'id': 3, 'name': 'VIETTEL'}, {'id': 4, 'name': 'VIETNAMOBILE'}, {'id': 5, 'name': 'ITELECOM'}, {'id': 6, 'name': 'VODAFONE_RO'}, {'id': 7, 'name': 'WINTEL'}, {'id': 8, 'name': 'METFONE'}, {'id': 9, 'name': 'UNITEL'}, {'id': 10, 'name': 'ETL'}, {'id': 11, 'name': 'BEELINE'}, {'id': 12, 'name': 'LAOTEL'}, {'id': 13, 'name': 'GTEL'}]}

# {'status_code': 200, 'message': 'successful', 'success': True, 'data': {'ID': 470362368, 'ServiceID': 45, 'ServiceName': 'WhatsApp - WhatsApp Business', 'Price': 3900, 'SmsContent': None, 'Status': 0, 'CreatedTime': '2025-05-10T22:05:08.833', 'IsSound': False, 'Code': None, 'PhoneOriginal': '0947546984', 'Phone': '947546984', 'CountryISO': 'VN', 'CountryCode': '84'}}

# {'status_code': 200, 'message': 'successful', 'success': True, 'data': {'ID': 470360613, 'ServiceID': 7, 'ServiceName': 'Facebook', 'Price': 1200, 'SmsContent': None, 'Status': 2, 'CreatedTime': '2025-05-10T21:58:10.517', 'IsSound': False, 'Code': None, 'PhoneOriginal': '0813042280', 'Phone': '813042280', 'CountryISO': 'VN', 'CountryCode': '84'}}

# {'status_code': 200, 'message': 'Tạo yêu cầu thành công !', 'success': True, 'data': {'phone_number': '824400262', 're_phone_number': '0824400262', 'countryISO': 'VN', 'countryCode': '84', 'request_id': 470364012, 'balance': 16800}}

# {'status_code': 200, 'message': 'successful', 'success': True, 'data': {'ID': 470364012, 'ServiceID': 45, 'ServiceName': 'WhatsApp - WhatsApp Business', 'Price': 3900, 'SmsContent': "Your WhatsApp code: 131075\n\nDon't share this code with others", 'Status': 1, 'CreatedTime': '2025-05-10T22:14:18.417', 'IsSound': False, 'Code': '131075', 'PhoneOriginal': '0824400262', 'Phone': '824400262', 'CountryISO': 'VN', 'CountryCode': '84'}}








































# durianrcs



# 0097	Gmail



name = 'Mohammedsn'
api_key = 'WTg1SnBQdTJ6ODFkYy9rS1dEc2ZEQT09'

# url = f'https://api.durianrcs.com/out/ext_api/getUserInfo?name={name}&ApiKey={api_key}'
# url = f'https://api.durianrcs.com/out/ext_api/getMobile?name={name}&ApiKey={api_key}&cuy=th&pid=0107&num=1&serial=2'  #0107  #0097



{'code': 200, 'msg': 'Success', 'data': '+66960844759'}



{'code': 200, 'msg': 'Success', 'data': '+66988354527'}

{'code': 200, 'msg': 'Success', 'data': '+66649949278'}

{'code': 200, 'msg': 'Success', 'data': '+66869699653'}

{'code': 200, 'msg': 'Success', 'data': '+18094960867'}

{'code': 906, 'msg': 'number list is empty', 'data': ''}

{'code': 200, 'msg': 'Success', 'data': '+66810264146'}
{'code': 200, 'msg': 'Success', 'data': '+66950975954'}
{'code': 200, 'msg': 'Success', 'data': '+6285282551690'}

# url = f'https://api.durianrcs.com/out/ext_api/getMobileCode?name={name}&ApiKey={api_key}&pid=1&num=5&noblack=0&serial=2&secret_key=null&vip=null'
url = f'https://api.durianrcs.com/out/ext_api/getMsg?name={name}&ApiKey={api_key}&pn=+66960844759&pid=0107&serial=2'

{'code': 908, 'msg': 'SMS not found. Please try again later', 'data': ''}
{'code': 405, 'msg': 'Failed to receive SMS. Please check the Message Record or contact the administrator', 'data': ''}

{'code': 200, 'msg': 'Success', 'data': '167328'}

# url = f'https://api.durianrcs.com/out/ext_api/getStatus?name={name}&ApiKey={api_key}&pn=+66964428658&pid=0107'

{'code': 203, 'msg': 'Number is not occupied, SMS not received', 'data': ''}
{'code': 202, 'msg': 'Number is occupied, SMS not received', 'data': None}


# url = f'https://api.durianrcs.com/out/ext_api/passMobile?name={name}&ApiKey={api_key}&pn=+66960844759&pid=0107&serial=2'

{'code': 200, 'msg': 'Success', 'data': ''}


# url = f'https://api.durianrcs.com/out/ext_api/getCountryPhoneNum?name={name}&ApiKey={api_key}&pid=0107&vip=null'

# response = requests.get(url)
# print(response)
# print(response.json())



{'code': 403, 'msg': 'Insufficient credits balance, please recharge to continue', 'data': ''}



{'code': 200, 'msg': 'Success', 'data': '+66840462262'}
{'code': 200, 'msg': 'Success', 'data': ['+66654898771', '+66946821392']}

{'code': 200, 'msg': 'Success', 'data': '+584120287208'}

{'code': 200, 'msg': 'Success', 'data': '+66984138932'}

{'code': 200, 'msg': 'Success', 'data': {'za': 430, 'ru': 219, 'mx': 158, 'ar': 120, 'th': 97, 've': 95, 'ly': 86, 'ao': 84, 'id': 74, 'ke': 64, 'us': 55, 'gh': 43, 'jm': 38, 'co': 33, 'dz': 33, 'sy': 28, 'br': 26, 'ng': 24, 'pk': 22, 'tn': 22, 'jo': 22, 'tt': 19, 'cu': 19, 'iq': 17, 'gt': 17, 'gb': 17, 'ca': 17, 'na': 17, 'mr': 16, 'kz': 15, 'it': 15, 'cg': 14, 'bd': 14, 'de': 12, 'uz': 12, 'np': 10, 'mz': 10, 'sn': 8, 'lb': 8, 'my': 7, 'am': 7, 'sd': 7, 'ph': 6, 'pt': 6, 'af': 6, 'pl': 6, 'tg': 6, 'mg': 6, 'ro': 5, 'kw': 5, 'bf': 5, 'td': 5, 'zw': 4, 'sa': 4, 'es': 4, 'ls': 4, 'ma': 4, 'cd': 4, 'sv': 4, 'mw': 4, 'ht': 4, 'ag': 3, 'lk': 3, 'tr': 3, 'sz': 3, 'ec': 2, 'cw': 2, 'mm': 2, 'cf': 2, 'in': 2, 'by': 2, 'pg': 2, 'vn': 2, 'ae': 2, 'lr': 1, 'gn': 1, 'sc': 1, 'pa': 1, 'bb': 1, 'ug': 1, 'bz': 1, 'gw': 1, 're': 1, '': 1, 'kh': 1, 'la': 1, 'il': 1, 'ch': 1, 'ss': 1, 'ba': 1, 'gq': 1, 'ir': 1, 'ne': 1, 'qa': 1, 'mv': 1, 'gp': 1}}





























# drop sms

api_key = 'aecafb0c-7f3d-4c2f-84c7-2bc9339d1c6a'

# api_key = '7b0279bb-ff4f-4a1d-b039-9b0c75f517b9'

# url = f'https://api.dropsms.cc/stubs/handler_api.php?action=getBalance&api_key={api_key}'

serviceid = 'wa'
idcountry = '110'
# url = f'https://api.dropsms.cc/stubs/handler_api.php?action=getNumber&api_key={api_key}&service={serviceid}&country=bo'

{"detail":"NO_BALANCE"}

# ACCESS_NUMBER:83504afee25c43b8918d3d642837dbdd:79515595631    25
# ACCESS_NUMBER:b55b160fcfb240af9ed6146a31c68d15:79025605548
# ACCESS_NUMBER:5792bef24ae249fb8f59eb3c805e343c:79531341203

# ACCESS_NUMBER:893d163453e44db4b15590f09741f04e:22871102906

# ACCESS_NUMBER:8ed14ef99dbb472d8cc37acf2738f73a:79011616993

# ACCESS_NUMBER:9691c105c03349b1969b84e37a727eef:79026759361

# ACCESS_NUMBER:148006b8725e434b86664e9f674431e7:79777148512

# ACCESS_NUMBER:ac496f74dc284a5a9a095841d9a9c0b3:79915936303

# ACCESS_NUMBER:dd995d39759c490fa6e9ba07b90342a7:59165353818
id = 'dd995d39759c490fa6e9ba07b90342a7'

# url = f'https://api.dropsms.cc/stubs/handler_api.php?action=getStatus&api_key={api_key}&id={id}'



# url = f'https://api.dropsms.cc/stubs/handler_api.php?action=getBest&api_key={api_key}&service={serviceid}'

# response = requests.get(url)
# print(response)
# print(response.text)
# print(response.json())

# STATUS_WAIT_CODE
# STATUS_OK:437318
















# import pycountry

# text = """ 
# 0 - Russia
# 1 - Ukraine
# 2 - Kazakhstan
# 3 - China
# 4 - Philippines
# 5 - Myanmar
# 6 - Indonesia
# 7 - Malaysia
# 8 - Kenya
# 9 - Tanzania
# 10 - Vietnam
# 11 - Kyrgyzstan
# 12 - USA
# 13 - Israel
# 14 - Hong Kong
# 15 - Poland
# 16 - Great Britain
# 17 - Madagascar
# 18 - Congo
# 19 - Nigeria
# 20 - Macau
# 21 - Egypt
# 22 - India
# 23 - Ireland
# 24 - Cambodia
# 25 - Laos
# 26 - Haiti
# 27 - Ivory Coast
# 28 - The Gambia
# 29 - Serbia
# 30 - Yemen
# 31 - South Africa
# 32 - Romania
# 33 - Colombia
# 34 - Estonia
# 35 - Azerbaijan
# 36 - Canada
# 37 - Morocco
# 38 - Ghana
# 39 - Argentina
# 40 - Uzbekistan
# 41 - Cameroon
# 42 - Chad
# 43 - Germany
# 44 - Lithuania
# 45 - Croatia
# 46 - Sweden
# 47 - Iraq
# 48 - The Netherlands
# 49 - Latvia
# 50 - Austria
# 51 - Belarus
# 52 - Thailand
# 53 - Saudi Arabia
# 54 - Mexico
# 55 - Taiwan
# 56 - Spain
# 57 - Iran
# 58 - Algeria
# 59 - Slovenia
# 60 - Bangladesh
# 61 - Senegal
# 62 - Turkey
# 63 - Czech Republic
# 64 - Sri Lanka
# 65 - Peru
# 66 - Pakistan
# 67 - New Zealand
# 68 - Guinea
# 69 - Mali
# 70 - Venezuela
# 71 - Ethiopia
# 72 - Mongolia
# 73 - Brazil
# 74 - Afghanistan
# 75 - Uganda
# 76 - Angola
# 77 - Cyprus
# 78 - France
# 79 - Papua New Guinea
# 80 - Mozambique
# 81 - Nepal
# 82 - Belgium
# 83 - Bulgaria
# 84 - Hungary
# 85 - Moldova
# 86 - Italy
# 87 - Paraguay
# 88 - Honduras
# 89 - Tunisia
# 90 - Nicaragua
# 91 - East Timor
# 92 - Bolivia
# 93 - Costa Rica
# 94 - Guatemala
# 95 - UAE
# 96 - Zimbabwe
# 97 - Puerto Rico
# 98 - Sudan
# 99 - Togo
# 100 - Kuwait
# 101 - El Salvador
# 102 - Libya
# 103 - Jamaica
# 104 - Trinidad and Tobago
# 105 - Ecuador
# 106 - Eswatini
# 107 - Oman
# 108 - Bosnia and Herzegovina
# 109 - Dominican Republic
# 110 - Syria
# 111 - Qatar
# 112 - Panama
# 113 - Cuba
# 114 - Mauritania
# 115 - Sierra Leone
# 116 - Jordan
# 117 - Portugal
# 118 - Barbados
# 119 - Burundi
# 120 - Benin
# 123 - Botswana
# 128 - Georgia
# 129 - Greece
# 130 - Guinea-Bissau
# 131 - Guyana
# 134 - Saint Kitts and Nevis
# 135 - Liberia
# 136 - Lesotho
# 137 - Malawi
# 138 - Namibia
# 140 - Rwanda
# 141 - Slovakia
# 142 - Suriname
# 143 - Tajikistan
# 145 - Bahrain
# 146 - Reunion
# 147 - Zambia
# 148 - Armenia
# 149 - Somalia
# 151 - Chile
# 152 - Burkina Faso
# 154 - Gabon
# 155 - Albania
# 156 - Uruguay
# 157 - Mauritius
# 158 - Bhutan
# 159 - Maldives
# 160 - Guadeloupe
# 161 - Turkmenistan
# 162 - French Guiana
# 163 - Finland
# 164 - Saint Lucia
# 165 - Luxembourg
# 166 - Saint Vincent and the Grenadines
# 167 - Equatorial Guinea
# 168 - Djibouti
# 169 - Antigua and Barbuda
# 170 - Cayman Islands
# 171 - Montenegro
# 173 - Switzerland
# 174 - Norway
# 175 - Australia
# 176 - Eritrea
# 177 - South Sudan
# 178 - Sao Tome and Principe
# 179 - Aruba
# 180 - Montserrat
# 181 - Anguilla
# 182 - Japan
# 183 - North Macedonia
# 184 - Seychelles
# 185 - New Caledonia
# 186 - Cape Verde
# 200 - South Korea
# """

# flist = text.split('\n')[1:-1]


# country_names = [ s.split('-')[1].strip() for s in flist]
# codes = [s.split('-')[0].strip() for s in flist]




# # # # Function to find ISO code for a country name
# # def get_iso_code(country_name):
# #     try:
# #         country = pycountry.countries.lookup(country_name)
# #         return country.alpha_2
# #     except LookupError:
# #         return None  # Handle missing names gracefully
    
# # country_codes = {}
# # c = []

# # for i in range(len(country_names)) :
# #     code = get_iso_code(country_names[i])
# #     country_codes[codes[i]] = code
# #     c.append(code)

# # print(c)

# # # Create dictionary with flags
# # country_flags = {
# #     name: "".join([chr(127462 + ord(c) - ord('A')) for c in get_iso_code(name)])
# #     for name in country_names if get_iso_code(name)
# # }

# # # Print results
# # print(country_flags)
 
# # names = {}


# # # from googletrans import Translator
# # # import asyncio

# # # translator = Translator()

# # # async def trans(name) :
# # #     return await translator.translate(name, src="en", dest="ar")


# # # for i in range(len(codes)) :
# # #     try :
# # #         names[codes[i]] = f"{asyncio.run(trans(country_names[i]))} {country_flags[country_names[i]]}"
# # #     except Exception as e :
# # #         print(e)
# # #         print(country_names[i])






# # import asyncio
# # from googletrans import Translator

# # async def translate_countries():
# #     translator = Translator()
    
# #     translated_countries = []
# #     for i in range(len(codes)) :

# #         translated = await translator.translate(country_names[i], src='en', dest='ar')
# #         transed = translated.text
# #         try :
# #             names[codes[i]] = f"{transed} {country_flags[country_names[i]]}"
# #         except Exception as e :
# #             print(e)
# #         # You must await the translate call
        

# # # Run the async function
# # asyncio.run(translate_countries())


# with open('prices.json' , 'r' , encoding='utf-8') as ff :
#     data = json.load(ff)


# with open('apps.json' , 'r' , encoding='utf-8') as fff :
#     data2 = json.load(fff)


# for country in data2['Whatsapp'] : 
#     print(country)
#     if country != 'vn' :
#         for id in data2['Whatsapp'][country]['drop_sms'] :
#             data['Whatsapp'][country] = {}
#             data['Whatsapp'][country]['drop_sms'] = {}
#             data['Whatsapp'][country]['drop_sms'][id] = 1

# for country in data2['Google'] : 
#     if country != 'vn' :
#         for id in data2['Google'][country]['drop_sms'] :
#             data['Google'][country] = {}
#             data['Google'][country]['drop_sms'] = {}
#             data['Google'][country]['drop_sms'][id] = 1



# # with open('prices.json' , 'w' , encoding='utf-8') as n :
# #     json.dump(data , n)










# drop sms

api_key = 'gBQb39jN3ZiOUHoGuuoGphGCmZrUB3S0nyRft7f7'

# api_key = '7b0279bb-ff4f-4a1d-b039-9b0c75f517b9'

# url = f'https://api.dropsms.cc/stubs/handler_api.php?action=getBalance&api_key={api_key}'

serviceid = 'go'
idcountry = '40'
# url = f'https://api.smslive.pro/stubs/handler_api.php?api_key={api_key}&action=getNumber&service={serviceid}&country={idcountry}'

id = '19054361706'
url = f'https://api.smslive.pro/stubs/handler_api.php?api_key={api_key}&action=setStatus&status=8&id={id}'
# ACCESS_CANCEL


# ACCESS_NUMBER:19054361706:6285712247871


# ACCESS_NUMBER:18470791184:963992522795

# ACCESS_NUMBER:18477033720:6283897814940

# ACCESS_NUMBER:18477148057:50943107245

{"detail":"NO_BALANCE"}



# url = f'https://api.smslive.pro/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={id}'

# NO_BALANCE

# url = f'https://api.dropsms.cc/stubs/handler_api.php?action=getBest&api_key={api_key}&service={serviceid}'


# url = f'https://api.smslive.pro/stubs/handler_api.php?api_key={api_key}&action=getNumbersStatus&country=$country=0'

# url = f'https://api.smslive.pro/stubs/handler_api.php?api_key={api_key}&action=getBalance'

# response = requests.get(url)
# print(response)
# print(response.text)
# print(response.json())

# STATUS_WAIT_CODE
# STATUS_OK:437318

# STATUS_WAIT_CODE

# NO_ACTIVATION


# ACCESS_NUMBER:18492805868:6285156044341

# ACCESS_BALANCE:1.104














# dur = """
# 1	Argentinas	阿根廷	ar	arg	54
# 2	Australia	澳大利亚	au	aus	61
# 3	Austria	奥地利	at	aut	43
# 4	Bahrain	巴林	bh	bhr	973
# 5	Brazil	巴西	br	bra	55
# 6	Chile	智利	cl	chl	56
# 7	Colombia	哥伦比亚	co	col	57
# 8	Czech Republic	捷克共和国	cz	cze	420
# 9	Ecuador	厄瓜多尔	ec	ecu	593
# 10	Finland	芬兰	fi	fin	358
# 11	France	法国	fr	fra	33
# 12	Germany	德国	de	deu	49
# 13	Ghana	加纳	gh	gha	233
# 14	Hungary	匈牙利	hu	hun	36
# 15	India	印度	in	ind	91
# 16	Indonesia	印度尼西亚	id	idn	62
# 17	Ireland	爱尔兰	ie	irl	353
# 18	Japan	日本	jp	jpn	81
# 19	Jordan	约旦	jo	jor	962
# 20	Kenya	肯尼亚	ke	ken	254
# 21	Luxembourg	卢森堡	lu	lux	352
# 22	Malaysia	马来西亚	my	mys	60
# 23	Mexico	墨西哥	mx	mex	52
# 24	Netherlands	荷兰	nl	nld	31
# 25	Nigeria	尼日利亚	ng	nga	234
# 26	Norway	挪威	no	nor	47
# 27	Panama	巴拿马	pa	pan	507
# 28	Philippines	菲律宾	ph	phl	63
# 29	Poland	波兰	pl	pol	48
# 30	Portugal	葡萄牙	pt	prt	351
# 31	Romania	罗马尼亚	ro	rou	40
# 32	Saudi Arabia	沙特阿拉伯	sa	sau	966
# 33	Singapore	新加坡	sg	sgp	65
# 34	Viet nam	越南	vn	vnm	84
# 35	Slovenia	斯洛文尼亚	si	svn	386
# 36	South Africa	南非	za	zaf	27
# 37	Spain	西班牙	es	esp	34
# 38	Switzerland	瑞士	ch	che	41
# 39	Thailand	泰国	th	tha	66
# 40	United Arab Emirates	阿拉伯联合酋长国	ae	are	971
# 41	Macedonia - The Frm Yugoslav Rep Of	马其顿,前南斯拉夫共和国	mk	mkd	389
# 42	Egypt	埃及	eg	egy	20
# 43	United States	美国	us	usa	1
# 44	Andorra	安道尔	ad	and	376
# 45	Afghanistan	阿富汗	af	afg	93
# 46	Antigua and Barbuda	安提瓜和巴布达	ag	atg	1268
# 47	Anguilla	安圭拉岛	ai	aia	1264
# 48	Albania	阿尔巴尼亚	al	alb	355
# 49	Armenia	亚美尼亚	am	arm	374
# 50	Angola	安哥拉	ao	ago	244
# 51	American Samoa	美属萨摩亚	as	asm	1684
# 52	Aruba	阿鲁巴	aw	abw	297
# 53	Azerbaijan	阿塞拜疆	az	aze	994
# 54	Bosnia and Herzegovina	波斯尼亚和黑塞哥维那	ba	bih	387
# 55	Barbados	巴巴多斯	bb	brb	1246
# 56	Bangladesh	孟加拉国	bd	bgd	880
# 57	Belgium	比利时	be	bel	32
# 58	Burkina Faso	布基纳法索	bf	bfa	226
# 59	Bulgaria	保加利亚	bg	bgr	359
# 60	Burundi	布隆迪	bi	bdi	257
# 61	Benin	贝宁	bj	ben	229
# 62	Bermuda	百慕大群岛	bm	bmu	1441
# 63	Brunei Darussalam	文莱	bn	brn	673
# 64	Bolivia, Plurinational State of	玻利维亚	bo	bol	591
# 65	Bahamas	巴哈马	bs	bhs	1242
# 66	Bhutan	不丹	bt	btn	975
# 67	Botswana	博茨瓦纳	bw	bwa	267
# 68	Belarus	白俄罗斯	by	blr	375
# 69	Belize	伯利兹	bz	blz	501
# 70	Canada	加拿大	ca	can	1
# 71	Congo, the Democratic Republic of the	刚果民主共和国	cd	cod	243
# 72	Central African Republic	中非共和国	cf	caf	236
# 73	Congo	刚果	cg	cog	242
# 74	Cote d'Ivoire/Ivory Coast	科特迪瓦	ci	civ	225
# 75	Cook Islands	库克群岛	ck	cok	682
# 76	Cameroon	喀麦隆	cm	cmr	237
# 77	Costa Rica	哥斯达黎加	cr	cri	506
# 78	Cuba	古巴	cu	cub	53
# 79	Cape Verde	佛得角	cv	cpv	238
# 80	Curaçao	库拉索	cw	cuw	5999
# 81	Cyprus	塞浦路斯	cy	cyp	357
# 82	Djibouti	吉布提	dj	dji	253
# 83	Denmark	丹麦	dk	dnk	45
# 84	Dominica	多米尼克	dm	dma	1767
# 85	Dominican Republic	多米尼加共和国	do	dom	1809
# 86	Algeria	阿尔及利亚	dz	dza	213
# 87	Estonia	爱沙尼亚	ee	est	372
# 88	Eritrea	厄立特里亚	er	eri	291
# 89	Ethiopia	埃塞俄比亚	et	eth	251
# 90	Fiji	斐济群岛	fj	fji	679
# 91	Falkland Islands (Malvinas)	福克兰群岛(马尔维纳斯群岛)	fk	flk	500
# 92	Micronesia, Federated States of	密克罗尼西亚	fm	fsm	691
# 93	Faroe Islands	法罗群岛	fo	fro	298
# 94	Gabon	加蓬	ga	gab	241
# 95	United Kingdom	英国	gb	gbr	44
# 96	Grenada	格林纳达	gd	grd	1473
# 97	Georgia	乔治亚	ge	geo	995
# 98	French Guiana	法属圭亚那	gf	guf	594
# 99	Gibraltar	直布罗陀	gi	gib	350
# 100	Greenland	格陵兰	gl	grl	299
# 101	Gambia	冈比亚	gm	gmb	220
# 102	Guinea	几内亚	gn	gin	224
# 103	Equatorial Guinea	赤道几内亚	gq	gnq	240
# 104	Greece	希腊	gr	grc	30
# 105	Guatemala	危地马拉	gt	gtm	502
# 106	Guam	关岛	gu	gum	1671
# 107	Guinea-Bissau	几内亚比绍	gw	gnb	245
# 108	Guyana	圭亚那	gy	guy	592
# 109	Honduras	洪都拉斯	hn	hnd	504
# 110	Croatia	克罗地亚	hr	hrv	385
# 111	Haiti	海地	ht	hti	509
# 112	Israel	以色列	il	isr	972
# 113	Iraq	伊拉克	iq	irq	964
# 114	Iran, Islamic Republic of	伊朗	ir	irn	98
# 115	Iceland	冰岛	is	isl	354
# 116	Italy	意大利	it	ita	39
# 117	Jamaica	牙买加	jm	jam	1876
# 118	Kyrgyzstan	吉尔吉斯斯坦	kg	kgz	996
# 119	Cambodia	柬埔寨	kh	khm	855
# 120	Kiribati	基里巴斯	ki	kir	686
# 121	Comoros	科摩罗	km	com	269
# 122	Saint Kitts and Nevis	圣基茨和尼维斯	kn	kna	1869
# 123	Korea, Democratic People's Republic of	朝鲜	kp	prk	850
# 124	Korea, Republic of	韩国	kr	kor	82
# 125	Kuwait	科威特	kw	kwt	965
# 126	Cayman Islands	开曼群岛	ky	cym	1345
# 127	Kazakhstan	哈萨克斯坦	kz	kaz	7
# 128	Lao People's Democratic Republic	老挝	la	lao	856
# 129	Lebanon	黎巴嫩	lb	lbn	961
# 130	Saint Lucia	圣卢西亚	lc	lca	1758
# 131	Liechtenstein	列支敦士登	li	lie	423
# 132	Sri Lanka	斯里兰卡	lk	lka	94
# 133	Liberia	利比里亚	lr	lbr	231
# 134	Lesotho	莱索托	ls	lso	266
# 135	Lithuania	立陶宛	lt	ltu	370
# 136	Latvia	拉脱维亚	lv	lva	371
# 137	Libya	利比亚	ly	lby	218
# 138	Morocco	摩洛哥	ma	mar	212
# 139	Monaco	摩纳哥	mc	mco	377
# 140	Moldova, Republic of	摩尔多瓦	md	mda	373
# 141	Montenegro	门的内哥罗(黑山)	me	mne	382
# 142	Madagascar	马达加斯加	mg	mdg	261
# 143	Marshall Islands	马绍尔群岛	mh	mhl	692
# 144	Mali	马里	ml	mli	223
# 145	Myanmar	缅甸	mm	mmr	95
# 146	Mongolia	蒙古	mn	mng	976
# 147	Macao	中国澳门	mo	mac	853
# 148	Northern Mariana Islands	北马里亚纳群岛	mp	mnp	1670
# 149	Martinique	马提尼克岛	mq	mtq	596
# 150	Mauritania	毛里塔尼亚	mr	mrt	222
# 151	Montserrat	蒙特塞拉特	ms	msr	1664
# 152	Malta	马耳他	mt	mlt	356
# 153	Mauritius	毛里求斯	mu	mus	230
# 154	Maldives	马尔代夫	mv	mdv	960
# 155	Malawi	马拉维	mw	mwi	265
# 156	Mozambique	莫桑比克	mz	moz	258
# 157	Namibia	纳米比亚	na	nam	264
# 158	New Caledonia	新喀里多尼亚	nc	ncl	687
# 159	Niger	尼日尔	ne	ner	227
# 160	Nicaragua	尼加拉瓜	ni	nic	505
# 161	Nepal	尼泊尔	np	npl	977
# 162	Nauru	瑙鲁	nr	nru	674
# 163	Niue	纽埃	nu	niu	683
# 164	New Zealand	新西兰	nz	nzl	64
# 165	Oman	阿曼	om	omn	968
# 166	Peru	秘鲁	pe	per	51
# 167	French Polynesia	法属波利尼西亚	pf	pyf	689
# 168	Papua New Guinea	巴布亚新几内亚	pg	png	675
# 169	Pakistan	巴基斯坦	pk	pak	92
# 170	Saint Pierre and Miquelon	圣皮埃尔岛和密克隆岛	pm	spm	508
# 171	Puerto Rico	波多黎各	pr	pri	1787
# 172	Palestine, State of	巴勒斯坦当局	ps	pse	970
# 173	Palau	帕劳群岛	pw	plw	680
# 174	Paraguay	巴拉圭	py	pry	595
# 175	Qatar	卡塔尔	qa	qat	974
# 176	Reunion	留尼汪岛	re	reu	262
# 177	Serbia	塞尔维亚	rs	srb	381
# 178	Russian Federation	俄罗斯	ru	rus	7
# 179	Rwanda	卢旺达	rw	rwa	250
# 180	Solomon Islands	所罗门群岛	sb	slb	677
# 181	Seychelles	塞舌尔	sc	syc	248
# 182	Sudan	苏丹	sd	sdn	249
# 183	Sweden	瑞典	se	swe	46
# 184	Slovakia	斯洛伐克	sk	svk	421
# 185	Sierra Leone	塞拉利昂	sl	sle	232
# 186	San Marino	圣马力诺	sm	smr	378
# 187	Senegal	塞内加尔	sn	sen	221
# 188	Somalia	索马里	so	som	252
# 189	Suriname	苏里南	sr	sur	597
# 190	South Sudan	南苏丹共和国	ss	ssd	+211
# 191	Sao Tome and Principe	圣多美和普林西比	st	stp	239
# 192	El Salvador	萨尔瓦多	sv	slv	503
# 193	Syrian Arab Republic	叙利亚	sy	syr	963
# 194	Swaziland	斯威士兰	sz	swz	268
# 195	Turks and Caicos Islands	特克斯群岛和凯科斯群岛	tc	tca	1649
# 196	Chad	乍得	td	tcd	235
# 197	Togo	多哥	tg	tgo	228
# 198	Tajikistan	塔吉克斯坦	tj	tjk	992
# 199	Timor-Leste	东帝汶	tl	tls	670
# 200	Turkmenistan	土库曼斯坦	tm	tkm	993
# 201	Tunisia	突尼斯	tn	tun	216
# 202	Tonga	汤加	to	ton	676
# 203	Turkey	土耳其	tr	tur	90
# 204	Trinidad and Tobago	特立尼达和多巴哥	tt	tto	1868
# 205	Tanzania, United Republic of	坦桑尼亚	tz	tza	255
# 206	Ukraine	乌克兰	ua	ukr	380
# 207	Uganda	乌干达	ug	uga	256
# 208	Uruguay	乌拉圭	uy	ury	598
# 209	Uzbekistan	乌兹别克斯坦	uz	uzb	998
# 210	Holy See (Vatican City State)	梵蒂冈城	va	vat	379
# 211	Saint Vincent and the Grenadines	圣文森特和格林纳丁斯	vc	vct	1784
# 212	Venezuela, Bolivarian Republic of	委内瑞拉	ve	ven	58
# 213	Virgin Islands, British	维尔京群岛（英属）	vg	vgb	1284
# 214	Virgin Islands, U.S.	维尔京群岛	vi	vir	1340
# 215	Vanuatu	瓦努阿图	vu	vut	678
# 216	Wallis and Futuna	瓦利斯群岛和富图纳群岛	wf	wlf	681
# 217	Samoa	萨摩亚	ws	wsm	685
# 218	Yemen	也门	ye	yem	967
# 219	Zambia	赞比亚	zm	zmb	260
# 220	Zimbabwe	津巴布韦	zw	zwe	263
# """

# rows = dur.strip().splitlines()
# parsed = [line.split('\t') for line in rows]
# print(parsed)


# d = [['1', 'Argentinas', '阿根廷', 'ar', 'arg', '54'], ['2', 'Australia', '澳大利亚', 'au', 'aus', '61'], ['3', 'Austria', '奥地利', 'at', 'aut', '43'], ['4', 'Bahrain', '巴林', 'bh', 'bhr', '973'], ['5', 'Brazil', '巴西', 'br', 'bra', '55'], ['6', 'Chile', '智利', 'cl', 'chl', '56'], ['7', 'Colombia', '哥伦比亚', 'co', 'col', '57'], ['8', 'Czech Republic', '捷克共和国', 'cz', 'cze', '420'], ['9', 'Ecuador', '厄瓜多尔', 'ec', 'ecu', '593'], ['10', 'Finland', '芬兰', 'fi', 'fin', '358'], ['11', 'France', '法国', 'fr', 'fra', '33'], ['12', 'Germany', '德国', 'de', 'deu', '49'], ['13', 'Ghana', '加纳', 'gh', 'gha', '233'], ['14', 'Hungary', '匈牙利', 'hu', 'hun', '36'], ['15', 'India', '印度', 'in', 'ind', '91'], ['16', 'Indonesia', '印度尼西亚', 'id', 'idn', '62'], ['17', 'Ireland', '爱尔兰', 'ie', 'irl', '353'], ['18', 'Japan', '日本', 'jp', 'jpn', '81'], ['19', 'Jordan', '约旦', 'jo', 'jor', '962'], ['20', 'Kenya', '肯尼亚', 'ke', 'ken', '254'], ['21', 'Luxembourg', '卢森堡', 'lu', 'lux', '352'], ['22', 'Malaysia', '马来西亚', 'my', 'mys', '60'], ['23', 'Mexico', '墨西哥', 'mx', 'mex', '52'], ['24', 'Netherlands', '荷兰', 'nl', 'nld', '31'], ['25', 'Nigeria', '尼日利亚', 'ng', 'nga', '234'], ['26', 'Norway', '挪威', 'no', 'nor', '47'], ['27', 'Panama', '巴拿马', 'pa', 'pan', '507'], ['28', 'Philippines', '菲律宾', 'ph', 'phl', '63'], ['29', 'Poland', '波兰', 'pl', 'pol', '48'], ['30', 'Portugal', '葡萄牙', 'pt', 'prt', '351'], ['31', 'Romania', '罗马尼亚', 'ro', 'rou', '40'], ['32', 'Saudi Arabia', '沙特阿拉伯', 'sa', 'sau', '966'], ['33', 'Singapore', '新加坡', 'sg', 'sgp', '65'], ['34', 'Viet nam', '越南', 'vn', 'vnm', '84'], ['35', 'Slovenia', '斯洛文尼亚', 'si', 'svn', '386'], ['36', 'South Africa', '南非', 'za', 'zaf', '27'], ['37', 'Spain', '西班牙', 'es', 'esp', '34'], ['38', 'Switzerland', '瑞士', 'ch', 'che', '41'], ['39', 'Thailand', '泰国', 'th', 'tha', '66'], ['40', 'United Arab Emirates', '阿拉伯联合酋长国', 'ae', 'are', '971'], ['41', 'Macedonia - The Frm Yugoslav Rep Of', '马其顿,前南斯拉夫共和国', 'mk', 'mkd', '389'], ['42', 'Egypt', '埃及', 'eg', 'egy', '20'], ['43', 'United States', '美国', 'us', 'usa', '1'], ['44', 'Andorra', '安道尔', 'ad', 'and', '376'], ['45', 'Afghanistan', '阿富汗', 'af', 'afg', '93'], ['46', 'Antigua and Barbuda', '安提瓜和巴布达', 'ag', 'atg', '1268'], ['47', 'Anguilla', '安圭拉岛', 'ai', 'aia', '1264'], ['48', 'Albania', '阿尔巴尼亚', 'al', 'alb', '355'], ['49', 'Armenia', '亚美尼亚', 'am', 'arm', '374'], ['50', 'Angola', '安哥拉', 'ao', 'ago', '244'], ['51', 'American Samoa', '美属萨摩亚', 'as', 'asm', '1684'], ['52', 'Aruba', '阿鲁巴', 'aw', 'abw', '297'], ['53', 'Azerbaijan', '阿塞拜疆', 'az', 'aze', '994'], ['54', 'Bosnia and Herzegovina', '波斯尼亚和黑塞哥维那', 'ba', 'bih', '387'], ['55', 'Barbados', '巴巴多斯', 'bb', 'brb', '1246'], ['56', 'Bangladesh', '孟加拉国', 'bd', 'bgd', '880'], ['57', 'Belgium', '比利时', 'be', 'bel', '32'], ['58', 'Burkina Faso', '布基纳法索', 'bf', 'bfa', '226'], ['59', 'Bulgaria', '保加 利亚', 'bg', 'bgr', '359'], ['60', 'Burundi', '布隆迪', 'bi', 'bdi', '257'], ['61', 'Benin', '贝宁', 'bj', 'ben', '229'], ['62', 'Bermuda', '百慕大群岛', 'bm', 'bmu', '1441'], ['63', 'Brunei Darussalam', '文莱', 'bn', 'brn', '673'], ['64', 'Bolivia, Plurinational State of', '玻利维亚', 'bo', 'bol', '591'], ['65', 'Bahamas', '巴哈马', 'bs', 'bhs', '1242'], ['66', 'Bhutan', '不丹', 'bt', 'btn', '975'], ['67', 'Botswana', '博茨瓦纳', 'bw', 'bwa', '267'], ['68', 'Belarus', '白俄罗斯', 'by', 'blr', '375'], ['69', 'Belize', '伯利兹', 'bz', 'blz', '501'], ['70', 'Canada', '加拿大', 'ca', 'can', '1'], ['71', 'Congo, the Democratic Republic of the', '刚果民主共和国', 'cd', 'cod', '243'], ['72', 'Central African Republic', '中非共和国', 'cf', 'caf', '236'], ['73', 'Congo', '刚果', 'cg', 'cog', '242'], ['74', "Cote d'Ivoire/Ivory Coast", '科特迪瓦', 'ci', 'civ', '225'], ['75', 'Cook Islands', '库克群岛', 'ck', 'cok', '682'], ['76', 'Cameroon', '喀麦隆', 'cm', 'cmr', '237'], ['77', 'Costa Rica', '哥斯 达黎加', 'cr', 'cri', '506'], ['78', 'Cuba', '古巴', 'cu', 'cub', '53'], ['79', 'Cape Verde', '佛得角', 'cv', 'cpv', '238'], ['80', 'Curaçao', '库拉索', 'cw', 'cuw', '5999'], ['81', 'Cyprus', '塞浦路斯', 'cy', 'cyp', '357'], ['82', 'Djibouti', '吉布提', 'dj', 'dji', '253'], ['83', 'Denmark', '丹麦', 'dk', 'dnk', '45'], ['84', 'Dominica', '多米尼克', 'dm', 'dma', '1767'], ['85', 'Dominican Republic', '多米尼加共和国', 'do', 'dom', '1809'], ['86', 'Algeria', '阿尔及利亚', 'dz', 'dza', '213'], ['87', 'Estonia', '爱沙尼亚', 'ee', 'est', '372'], ['88', 'Eritrea', '厄立特里亚', 'er', 'eri', '291'], ['89', 'Ethiopia', '埃塞俄比亚', 'et', 'eth', '251'], ['90', 'Fiji', '斐济群岛', 'fj', 'fji', '679'], ['91', 'Falkland Islands (Malvinas)', '福克兰群岛(马尔维纳斯群岛)', 'fk', 'flk', '500'], ['92', 'Micronesia, Federated States of', '密克罗尼西亚', 'fm', 'fsm', '691'], ['93', 'Faroe Islands', '法罗群岛', 'fo', 'fro', '298'], ['94', 'Gabon', '加蓬', 'ga', 'gab', '241'], ['95', 'United Kingdom', '英国', 'gb', 'gbr', '44'], ['96', 'Grenada', '格林纳达', 'gd', 'grd', '1473'], ['97', 'Georgia', '乔治亚', 'ge', 'geo', '995'], ['98', 'French Guiana', '法属圭亚那', 'gf', 'guf', '594'], ['99', 'Gibraltar', '直布罗陀', 'gi', 'gib', '350'], ['100', 'Greenland', '格陵兰', 'gl', 'grl', '299'], ['101', 'Gambia', '冈比亚', 'gm', 'gmb', '220'], ['102', 'Guinea', '几内亚', 'gn', 'gin', '224'], ['103', 'Equatorial Guinea', '赤道几内亚', 'gq', 'gnq', '240'], ['104', 'Greece', '希腊', 'gr', 'grc', '30'], ['105', 'Guatemala', '危地马拉', 'gt', 'gtm', '502'], ['106', 'Guam', '关岛', 'gu', 'gum', '1671'], ['107', 'Guinea-Bissau', '几内亚比绍', 'gw', 'gnb', '245'], ['108', 'Guyana', '圭亚那', 'gy', 'guy', '592'], ['109', 'Honduras', '洪都拉斯', 'hn', 'hnd', '504'], ['110', 'Croatia', '克罗地亚', 'hr', 'hrv', '385'], ['111', 'Haiti', '海地', 'ht', 'hti', '509'], ['112', 'Israel', '以色列', 'il', 'isr', '972'], ['113', 'Iraq', '伊拉克', 'iq', 'irq', '964'], ['114', 'Iran, Islamic Republic of', '伊朗', 'ir', 'irn', '98'], ['115', 'Iceland', '冰岛', 'is', 'isl', '354'], ['116', 'Italy', '意大利', 'it', 'ita', '39'], ['117', 'Jamaica', '牙买加', 'jm', 'jam', '1876'], ['118', 'Kyrgyzstan', '吉尔吉斯斯坦', 'kg', 'kgz', '996'], ['119', 'Cambodia', '柬埔寨', 'kh', 'khm', '855'], ['120', 'Kiribati', '基里巴斯', 'ki', 'kir', '686'], ['121', 'Comoros', '科摩罗', 'km', 'com', '269'], ['122', 'Saint Kitts and Nevis', '圣基茨和尼维斯', 'kn', 'kna', '1869'], ['123', "Korea, Democratic People's Republic of", '朝鲜', 'kp', 'prk', '850'], ['124', 'Korea, Republic of', '韩国', 'kr', 'kor', '82'], ['125', 'Kuwait', '科威特', 'kw', 'kwt', '965'], ['126', 'Cayman Islands', '开曼群岛', 'ky', 'cym', '1345'], ['127', 'Kazakhstan', '哈萨克斯坦', 'kz', 'kaz', '7'], ['128', "Lao People's Democratic Republic", '老挝', 'la', 'lao', '856'], ['129', 'Lebanon', '黎巴嫩', 'lb', 'lbn', '961'], ['130', 'Saint Lucia', '圣卢西亚', 'lc', 'lca', '1758'], ['131', 'Liechtenstein', '列支敦士登', 'li', 'lie', '423'], ['132', 'Sri Lanka', ' 斯里兰卡', 'lk', 'lka', '94'], ['133', 'Liberia', '利比里亚', 'lr', 'lbr', '231'], ['134', 'Lesotho', '莱索托', 'ls', 'lso', '266'], ['135', 'Lithuania', '立陶宛', 'lt', 'ltu', '370'], ['136', 'Latvia', '拉脱维亚', 'lv', 'lva', '371'], ['137', 'Libya', '利比亚', 'ly', 'lby', '218'], ['138', 'Morocco', '摩洛哥', 'ma', 'mar', '212'], ['139', 'Monaco', '摩纳哥', 'mc', 'mco', '377'], ['140', 'Moldova, Republic of', '摩尔多瓦', 'md', 'mda', '373'], ['141', 'Montenegro', '门的内哥罗(黑山)', 'me', 'mne', '382'], ['142', 'Madagascar', '马达加斯加', 'mg', 'mdg', '261'], ['143', 'Marshall Islands', '马绍尔群岛', 'mh', 'mhl', '692'], ['144', 'Mali', '马里', 'ml', 'mli', '223'], ['145', 'Myanmar', '缅甸', 'mm', 'mmr', '95'], ['146', 'Mongolia', '蒙古', 'mn', 'mng', '976'], ['147', 'Macao', '中国澳门', 'mo', 'mac', '853'], ['148', 'Northern Mariana Islands', '北马里亚纳群岛', 'mp', 'mnp', '1670'], ['149', 'Martinique', '马提尼克岛', 'mq', 'mtq', '596'], ['150', 'Mauritania', '毛里塔尼亚', 'mr', 'mrt', '222'], ['151', 'Montserrat', '蒙特塞拉特', 'ms', 'msr', '1664'], ['152', 'Malta', '马耳他', 'mt', 'mlt', '356'], ['153', 'Mauritius', '毛里求斯', 'mu', 'mus', '230'], ['154', 'Maldives', '马尔代夫', 'mv', 'mdv', '960'], ['155', 'Malawi', '马拉维', 'mw', 'mwi', '265'], ['156', 'Mozambique', '莫桑比克', 'mz', 'moz', '258'], ['157', 'Namibia', '纳米比亚', 'na', 'nam', '264'], ['158', 'New Caledonia', '新喀里多尼亚', 'nc', 'ncl', '687'], ['159', 'Niger', '尼日尔', 'ne', 'ner', '227'], ['160', 'Nicaragua', '尼加拉瓜', 'ni', 'nic', '505'], ['161', 'Nepal', '尼泊尔', 'np', 'npl', '977'], ['162', 'Nauru', '瑙鲁', 'nr', 'nru', '674'], ['163', 'Niue', '纽埃', 'nu', 'niu', '683'], ['164', 'New Zealand', '新西兰', 'nz', 'nzl', '64'], ['165', 'Oman', '阿曼', 'om', 'omn', '968'], ['166', 'Peru', '秘鲁', 'pe', 'per', '51'], ['167', 'French Polynesia', '法属波利尼西亚', 'pf', 'pyf', '689'], ['168', 'Papua New Guinea', '巴布亚新几内亚', 'pg', 'png', '675'], ['169', 'Pakistan', '巴基斯坦', 'pk', 'pak', '92'], ['170', 'Saint Pierre and Miquelon', '圣皮埃尔岛和密克隆岛', 'pm', 'spm', '508'], ['171', 'Puerto Rico', '波多黎各', 'pr', 'pri', '1787'], ['172', 'Palestine, State of', '巴勒斯坦当局', 'ps', 'pse', '970'], ['173', 'Palau', '帕劳群岛', 'pw', 'plw', '680'], ['174', 'Paraguay', '巴拉圭', 'py', 'pry', '595'], ['175', 'Qatar', '卡塔尔', 'qa', 'qat', '974'], ['176', 'Reunion', '留尼汪岛', 're', 'reu', '262'], ['177', 'Serbia', '塞尔维亚', 'rs', 'srb', '381'], ['178', 'Russian Federation', '俄罗斯', 'ru', 'rus', '7'], ['179', 'Rwanda', '卢旺达', 'rw', 'rwa', '250'], ['180', 'Solomon Islands', '所罗门群岛', 'sb', 'slb', '677'], ['181', 'Seychelles', '塞舌尔', 'sc', 'syc', '248'], ['182', 'Sudan', '苏丹', 'sd', 'sdn', '249'], ['183', 'Sweden', '瑞典', 'se', 'swe', '46'], ['184', 'Slovakia', '斯洛伐 克', 'sk', 'svk', '421'], ['185', 'Sierra Leone', '塞拉利昂', 'sl', 'sle', '232'], ['186', 'San Marino', '圣马力诺', 'sm', 'smr', '378'], ['187', 'Senegal', '塞内加尔', 'sn', 'sen', '221'], ['188', 'Somalia', '索马里', 'so', 'som', '252'], ['189', 'Suriname', '苏里南', 'sr', 'sur', '597'], ['190', 'South Sudan', '南苏丹共和国', 'ss', 'ssd', '+211'], ['191', 'Sao Tome and Principe', '圣多美和普林西比', 'st', 'stp', '239'], ['192', 'El Salvador', '萨尔瓦多', 'sv', 'slv', '503'], ['193', 'Syrian Arab Republic', '叙利亚', 'sy', 'syr', '963'], ['194', 'Swaziland', '斯威士兰', 'sz', 'swz', '268'], ['195', 'Turks and Caicos Islands', '特克斯群岛和凯科斯群岛', 'tc', 'tca', '1649'], ['196', 'Chad', '乍得', 'td', 'tcd', '235'], ['197', 'Togo', '多哥', 'tg', 'tgo', '228'], ['198', 'Tajikistan', '塔吉克斯坦', 'tj', 'tjk', '992'], ['199', 'Timor-Leste', '东帝汶', 'tl', 'tls', '670'], ['200', 'Turkmenistan', '土库曼斯坦', 'tm', 'tkm', '993'], ['201', 'Tunisia', '突尼斯', 'tn', 'tun', '216'], ['202', 'Tonga', '汤加', 'to', 'ton', '676'], ['203', 'Turkey', '土耳其', 'tr', 'tur', '90'], ['204', 'Trinidad and Tobago', '特立尼达和多巴哥', 'tt', 'tto', '1868'], ['205', 'Tanzania, United Republic of', '坦桑 a, United Republic of', '坦桑尼亚', 'tz', 'tza', '255'], ['206', 'Ukraine', '乌克兰', 'ua', 'ukr', '380'], ['207', 'Uganda', '乌干达', 'ug', 'uga', '256'], ['208', 'Uruguay', '乌拉圭', 'uy', 'ury', '598'], ['209', 'Uzbekistan', '乌兹别克斯坦', 'uz', 'uzb', '998'], ['210', 'Holy See (Vatican City State)', '梵蒂冈城', 'va', 'vat', '379'], ['211', 'Saint Vincent and the Grenadines', '圣文森特和格林纳丁斯', 'vc', 'vct', '1784'], ['212', 'Venezuela, Bolivarian Republic of', '委内瑞拉', 've', 'ven', '58'], ['213', 'Virgin Islands, British', '维尔京群岛（英属）', 'vg', 'vgb', '1284'], ['214', 'Virgin Islands, U.S.', '维尔京群岛', 'vi', 'vir', '1340'], ['215', 'Vanuatu', '瓦努阿图', 'vu', 'vut', '678'], ['216', 'Wallis and Futuna', '瓦利斯群岛和富图纳群岛', 'wf', 'wlf', '681'], ['217', 'Samoa', '萨摩 亚', 'ws', 'wsm', '685'], ['218', 'Yemen', '也门', 'ye', 'yem', '967'], ['219', 'Zambia', '赞比亚', 'zm', 'zmb', '260'], ['220', 'Zimbabwe', '津巴布韦', 'zw', 'zwe', '263']]

# with open('durancies.json' , 'r' , encoding='utf-8')as file :
#     data = json.load(file)

# data['all_countries'] = []

# for line in parsed :
#     country_code= line[3]
#     data['all_countries'].append(country_code)

# with open('durancies.json' , 'w' , encoding='utf-8')as new :
#     json.dump(data, new)


# with open('durancies.json' , 'r' , encoding='utf-8')as file :
#     data = json.load(file)

# with open('apps.json'  , 'r' , encoding='utf-8') as file :
#     prices = json.load(file)

# for country_code in data['all_countries'] :
#     if country_code.upper() in prices['Whatsapp'] :
#         prices['Whatsapp'][country_code.upper()]['duriancrs'] = []
#     else :
#         prices['Whatsapp'][country_code.upper()] = {}
#         prices['Whatsapp'][country_code.upper()]['duriancrs'] = []


# for country_code in data['all_countries'] :
#     if country_code.upper() in prices['Google'] :
#         prices['Google'][country_code.upper()]['duriancrs'] = []
#     else :
#         prices['Google'][country_code.upper()] = {}
#         prices['Google'][country_code.upper()]['duriancrs'] = []

# with open('apps.json' , 'w' , encoding='utf-8')as new :
#     json.dump(prices,new)
















# url = 'https://smmparty.com/api/v2'

# params = {
#     'key' : 'dab3fac7cde4ca03f835688b83789674',
#     'action' : 'status',
#     'order' : 664444
# }

# response = requests.get(url , params= params)
# print(response.json())

# {'charge': '0.00', 'start_count': '0', 'status': 'Canceled', 'remains': '1000', 'currency': 'USD'}

# {'charge': '0.12164', 'start_count': '435', 'status': 'Completed', 'remains': '0', 'currency': 'USD'}

# {'charge': '0.00349', 'start_count': '7', 'status': 'Partial', 'remains': '900', 'currency': 'USD'}




import sqlite3 
import json
import functions
# conn = functions.connect_db()
# cursor = conn.cursor()

# checked = []

# cursor.execute('''SELECT id , name , username , balance FROM users ''')
# users = cursor.fetchall()




# data = {}

# for user in users :
#     id , name, username , balance = user

#     total_expenses = balance 
#     total_balance = 0

#     cursor.execute('SELECT status , price , code FROM item_requests WHERE user_id = ?', (id,))
#     numbers_purchase = cursor.fetchall()

#     for op in numbers_purchase :
#         status , price , code = op
#         if status == 'منتهية' or status == 'مفعل' or code : 
#             total_expenses += price
    
#     cursor.execute('SELECT status , price FROM social_requests WHERE user_id = ? ',(id,))
#     social = cursor.fetchall()

#     for op in social :
#         status , price = op
#         if status == 'مقبول' : 
#             total_expenses += price
    
#     cursor.execute('SELECT amount_added , status FROM topup_requests WHERE user_id = ? ',(id,))
#     topup = cursor.fetchall()

#     for op in topup :
#         amount , status = op
#         if status == 'مقبول' or status == 'approved' :
#             if amount > 100 :
#                 amount = amount / 10500
#             total_balance += amount
    

#     cursor.execute('SELECT added_amount , type FROM added_manually WHERE user_id = ? ',(id,))
#     topup = cursor.fetchall()
    
    
#     for op in topup :
#         amount , type = op
#         if type == 'إضافة رصيد':
#             total_balance += amount
        
#         elif type == 'حذف رصيد':
#             total_balance -= amount

    
#     data[str(id)] = {}
#     data[str(id)]['name'] = name
#     data[str(id)]['username'] = username
#     data[str(id)]['balance'] = balance
#     data[str(id)]['expenses'] = total_expenses
#     data[str(id)]['topup'] = total_balance
#     data[str(id)]['has more'] = total_balance - total_expenses




# with open('record.json' , 'w' , encoding='utf-8') as file :
#     json.dump(data , file)

# 6306691535
# 5349543151
# 5363898935


conn = functions.connect_db()
cursor = conn.cursor()

def cal(user , cursor) :
    accepted_topup = 0
    successful_number_buy = 0
    successful_social_buy = 0
    added_removed_manual = 0

    cursor.execute('SELECT name , username , balance FROM users WHERE id = ?',(user,))
    data = cursor.fetchone()
    name, username ,balance = data

    cursor.execute('''SELECT amount_added FROM topup_requests WHERE user_id = ? AND (status = 'مقبول' OR status = 'approved' )''' , (user,))
    top = cursor.fetchall()
    for op in top :
        amount = op[0]
        
        if amount > 100 :
            amount = amount / 10500
        
        accepted_topup += amount
        

    cursor.execute('''SELECT request_id, price FROM item_requests WHERE (status = 'منتهية' OR status = 'مفعل' OR code IS NOT NULL) AND user_id = ? ''',(user,))
    numbers = cursor.fetchall()

    for op in numbers :
        req , price = op
        successful_number_buy += price
        print(req)
    

    cursor.execute('''SELECT price FROM social_requests WHERE status = 'مقبول'  AND user_id = ? ''',(user,))
    socials = cursor.fetchall()

    for op in socials :
        price = op[0]
        successful_social_buy += price
    

    cursor.execute('SELECT added_amount , type FROM added_manually WHERE user_id = ? ',(user,))
    manual = cursor.fetchall()

    for op in manual :
        amount , type = op
        if type == 'إضافة رصيد' :
            added_removed_manual += amount
        elif type == 'حذف رصيد' :
            added_removed_manual -= amount
    
    total_revenue = accepted_topup + added_removed_manual - balance - successful_number_buy - successful_social_buy  # if positive , we he needs , if negative, we need

    return name , username , balance , accepted_topup , added_removed_manual , successful_number_buy , successful_social_buy , total_revenue




# cursor.execute('SELECT id FROM users WHERE id <> 5349543151 AND id <> 5363898935 AND id <> 6313379271 AND id <> 1693441250 AND id <> 6306691535')
# users = cursor.fetchall()

# total = 0
# data = {}
# for user in users :
#     user = user[0]
#     name , username , balance , accepted_topup , added_removed_manual , successful_number_buy , successful_social_buy , total_revenue = cal(user , cursor )
#     total += total_revenue 
#     data[str(user)] = {}
#     data[str(user)]['name']  = name
#     data[str(user)]['username']  = username
#     data[str(user)]['balance']  = balance
#     data[str(user)]['accepted_topup']  = accepted_topup
#     data[str(user)]['added_removed_manual']  = added_removed_manual
#     data[str(user)]['successful_number_buy']  = successful_number_buy
#     data[str(user)]['successful_social_buy']  = successful_social_buy
#     data[str(user)]['total_revenue']  = total_revenue


# print(total)

# # with open('record.json' , 'w' , encoding= 'utf-8') as file :
# #     json.dump(data , file)



