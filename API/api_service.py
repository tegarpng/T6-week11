import requests

class APIservice:
    BASE_URL = "https://api.pahrul.my.id/api"
    TIMEOUT = 10
    
    def get_posts(self):
        response = requests.get(
            f"{self.BASE_URL}/posts",
            timeout=self.TIMEOUT
		)
        
        response.raise_for_status()
        return response.json()['data']
    
    def get_post(self, id):
        response = requests.get(
            f"{self.BASE_URL}/posts/{id}",
            timeout=self.TIMEOUT
		)
        
        response.raise_for_status()
        return response.json()['data']
    
    def create_post(self, title, body, author, slug, status):
        payload = {
            'title':title,
            'body':body,
            'author':author,
            'slug':slug,
            'status':status
		}
        response = requests.post(
            f"{self.BASE_URL}/posts",
            json=payload,       # otomatis set Content-Type: application/json
            timeout=self.TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    
    def update_post(self, id, title, body, author, slug, status):
        payload = {
            'title':title,
            'body':body,
            'author':author,
            'slug':slug,
            'status':status
		}
        response = requests.put(
            f"{self.BASE_URL}/posts/{id}",
            json=payload,       # otomatis set Content-Type: application/json
            timeout=self.TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    
    def delete_post(self, id):
        response = requests.delete(
            f"{self.BASE_URL}/posts/{id}",
            timeout=self.TIMEOUT
        )
        response.raise_for_status()
        return True