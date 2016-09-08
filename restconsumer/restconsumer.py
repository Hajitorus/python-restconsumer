import requests
# from functools import lru_cache


def append_to_url(base_url, param):
    return base_url + param + "/"


class RestConsumer(object):

    def __init__(self, base_url, append_slash=False, append_json=False, **kwargs):
        self.base_url = base_url
        if not self.base_url.endswith('/') and append_slash:
            self.base_url = self.base_url + '/'
        self.append_json = append_json
        self.append_slash = append_slash
        self.kwargs = kwargs

    def __getattr__(self, key):
        new_base = append_to_url(self.base_url, key)
        return self.__class__(base_url=new_base,
                              append_json=self.append_json,
                              append_slash=self.append_slash,
                              **self.kwargs)
    
    def __getitem__(self, key):
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        if self.append_json:
            self.base_url = self.base_url + '.json'
        kwargs.update(self.kwargs)
        return self.get(self.base_url, **kwargs)

    # @lru_cache()
    def get(self, url, **kwargs):
        return requests.get(url, **kwargs)

    def post(self, **kwargs):
        return requests.post(**kwargs)

    def cache_info(self):
        return self.get.cache_info()


# DONE: get auth munged in there somehow
# DONE: pass any requests-recognised kwargs in to __init__ or __call__
# DONE? probably maybe cache this stuff?!
# TODO: maybe fix append_slash semantics?


if __name__=='__main__':
    Twitter = RestConsumer(base_url='https://api.twitter.com/1', append_json=True)
    Github = RestConsumer(base_url='https://api.github.com')
    Stackoverflow = RestConsumer(base_url='http://api.stackoverflow.com/1.1')

    from pprint import pprint
    t = RestConsumer(base_url='https://api.twitter.com/1', append_json=True)
    public_timeline = t.statuses.public_timeline()
    pprint(public_timeline)

    g = RestConsumer(base_url='https://api.github.com')
    repos = g.users.kennethreitz.repos()
    pprint(repos)

    s = RestConsumer(base_url='http://api.stackoverflow.com/1.1')
    sr = s.users['55562'].questions.unanswered()
    pprint(sr)

    sr2 = s.tags.python['top-answerers']['all-time']
    pprint(sr2())
    
