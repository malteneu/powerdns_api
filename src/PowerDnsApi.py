from typing import Optional, Dict, Any, List
from requests import Request, Session, Response



class PowerDnsClient:

    def __init__(self, endpoint: str = 'http://127.0.0.1:8081/api/v1/', api_key: str = None) -> None:
        self._session = Session()
        self._create_header(api_key)
        self._ENDPOINT = endpoint

    def _create_header(self, api_key):
        self._headers = {"X-API-Key": api_key}

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('POST', path, json=params)

    def _patch(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('PATCH', path, json=params)

    def _delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('DELETE', path, json=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._ENDPOINT + path, self._headers, **kwargs)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except :
            data = response.raise_for_status()
        else:
            return data

    def get_servers(self):
        return self._get("servers")

    def get_server(self, server_id: str):
        return self._get("servers/" + server_id)

    def get_zones(self, server_id: str):
        return self._get("servers/" + server_id + "/zones")

    def _create_zone(self, kind: str, server_id: str, name: str, nameservers: Optional[List[str]] = None,
                     masters: Optional[List[str]] = None):
        url = "servers/" + server_id + "/zones"

        return self._post(url, {'kind': kind,
                                'soa_edit_api': 'INCEPTION-INCREMENT',
                                'name': name,
                                'nameservers': nameservers,
                                'masters': masters,
                                })

    def create_master_zone(self, server_id: str, name: str, nameservers: List[str]):
        return self._create_zone('Master', server_id, name, nameservers=nameservers)

    def create_native_zone(self, server_id: str, name: str, nameservers: List[str]):
        return self._create_zone('Native', server_id, name, nameservers=nameservers)

    def create_slave_zone(self, server_id: str, name: str, masters: List[str]):
        return self._create_zone('Slave', server_id, name, masters=masters)

    def delete_zone(self, server_id: str, name: str):
        url = "servers/" + server_id + "/zones/" + name
        self._delete(url)

    def get_zone(self, server_id: str, name: str):
        url = "servers/" + server_id + "/zones/" + name
        return self._get(url)

    def get_zone_records(self, server_id: str, name: str):
        return self.get_zone(server_id, name)["rrsets"]

    def _edit_record(self, changetype: str, server_id: str, name: str, type: str, content: str, record_name: str, ttl: str):
        url = "servers/" + server_id + "/zones/" + name
        if (record_name != ""):
            record_name = record_name + "." + name
        else:
            record_name = name

        payload = {
                    "rrsets": [
                        {
                            "name": record_name,
                            "type": type,
                            "ttl": ttl,
                            "changetype": changetype,
                            "records": [
                                {
                                    "content": content,
                                    "disabled": False,
                                }
                            ]
                        }
                    ]
                }
        return self._patch(url, payload)

    def create_record(self, server_id: str, name: str, type: str, content: str, record_name: str = "", ttl: str = '86400'):
        return self._edit_record('REPLACE', server_id, name, type, content, record_name, ttl)

    def create_soa_record(self, server_id: str, name: str, primary: str, email: str, refresh: str = '3600',
                          retry: str = '900', expire: str = '604800', ttl: str = '86400'):
        content = primary + ' ' + email + ' 2022020708 ' + refresh + ' ' + retry + ' ' + expire + ' ' + ttl
        print(content)
        return self._edit_record('REPLACE', server_id, name, "SOA", content, "", ttl)

    def edit_record(self, server_id: str, name: str, type: str, content: str, record_name: str = "", ttl: str = '86400'):
        return self._edit_record('REPLACE', server_id, name, type, content, record_name, ttl)

    def delete_record(self, server_id: str, name: str, record_name: str, type: str):
        return self._edit_record('DELETE', server_id, name, type, content=None, record_name=record_name, ttl=None)

if __name__ == "__main__":
    client = PowerDnsClient('http://127.0.0.1:8081/api/v1/', 'API Key')

    domain = 'domain.tld.'

    print(client.create_record('localhost', domain, 'A', '127.0.0.1', ''))
    print(client.create_record('localhost', domain, 'A', '127.0.0.1', 'www'))
    print(client.create_record('localhost', domain, 'AAAA', '::1', ''))
    print(client.create_record('localhost', domain, 'AAAA', '::1', 'www'))
