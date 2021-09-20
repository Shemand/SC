import json

if __name__ == '__main__':
    csv_file = open('crypto_gateways.csv', 'r')
    json_file = open('crypto_gateways.json', 'w')
    crypto_gateways = []
    for line in csv_file:
        data = list(map(lambda x: x.removesuffix('\n'), line.split('/')))
        crypto_gateways.append({
            "name": data[4],
            "caption": data[3],
            "unit": data[2],
            "ip": data[0],
            "mask": int(data[1]),
            "isActive": True if data[5] == '+' else False
        })
    csv_file.close()
    json_file.write(str(json.dumps(crypto_gateways, indent=4)))
    json_file.close()
    print('file created')