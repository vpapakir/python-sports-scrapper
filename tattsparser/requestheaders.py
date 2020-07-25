# create random request header
# https://github.com/FantomNet/DDoS/blob/master/BlackHorizon.py

import random
import time

USER_AGENT_PARTS = {
    'os': {
        'linux': {
            'name': ['Linux x86_64', 'Linux i386'],
            'ext': ['X11']
        },
        'windows': {
            'name': ['Windows NT 6.1', 'Windows NT 6.3', 'Windows NT 5.1', 
                    'Windows NT.6.2'],
            'ext': ['WOW64', 'Win64; x64']
        },
        'mac': {
            'name': ['Macintosh'],
            'ext': ['Intel Mac OS X %d_%d_%d' % (random.randint(10, 11), 
                    random.randint(0, 9), random.randint(0, 5)) 
                    for i in range(1, 10)]
        },
    },
    'platform': {
        'webkit': {
            'name': ['AppleWebKit/%d.%d' % (random.randint(535, 537), 
                        random.randint(1,36)) for i in range(1, 30)],
            'details': ['KHTML, like Gecko'],
            'extensions': ['Chrome/%d.0.%d.%d Safari/%d.%d' 
                            % (random.randint(6, 32), random.randint(100, 2000),
                            random.randint(0, 100), random.randint(535, 537), 
                            random.randint(1, 36)) for i in range(1, 30)] + 
                          ['Version/%d.%d.%d Safari/%d.%d' 
                            % (random.randint(4, 6), random.randint(0, 1), 
                            random.randint(0, 9), random.randint(535, 537), 
                            random.randint(1, 36)) for i in range(1, 10)]
        },
        'iexplorer': {
            'browser_info': {
                'name': ['MSIE 6.0', 'MSIE 6.1', 'MSIE 7.0', 'MSIE 7.0b', 
                            'MSIE 8.0', 'MSIE 9.0', 'MSIE 10.0'],
                'ext_pre': ['compatible', 'Windows; U'],
                'ext_post': ['Trident/%d.0' % i for i in range(4, 6)] + 
                            ['.NET CLR %d.%d.%d' % (random.randint(1, 3), 
                                random.randint(0, 5), 
                                random.randint(1000, 30000)) 
                                for i in range(1, 10)]
            }
        },
        'gecko': {
            'name': ['Gecko/%d%02d%02d Firefox/%d.0' 
                        % (random.randint(2001, 2010), random.randint(1,31), 
                        random.randint(1,12) , random.randint(10, 25)) 
                        for i in range(1, 30)],
            'details': [],
            'extensions': []
        }
    }
}


class Headers():

    #builds random ascii string
    def buildblock(self, size):
        out_str = ''

        _LOWERCASE = range(97, 122)
        _UPPERCASE = range(65, 90)
        _NUMERIC   = range(48, 57)

        validChars = _LOWERCASE + _UPPERCASE + _NUMERIC
        for i in range(0, size):
            a = random.choice(validChars)
            out_str += chr(a)

        return out_str


    def generateQueryString(self, ammount = 1):
        queryString = []
        for i in range(ammount):
            key = self.buildblock(random.randint(3,10))
            value = self.buildblock(random.randint(3,20))
            element = "{0}={1}".format(key, value)
            queryString.append(element)

        return '&'.join(queryString)


    def getUserAgent(self):
        # Mozilla/[version] ([system and browser information]) [platform] 
        # ([platform details]) [extensions]

        ## Mozilla Version
        # hardcoded for now, almost every browser is on this version except IE6
        mozilla_version = "Mozilla/5.0" 

        ## System And Browser Information
        # Choose random OS
        os = USER_AGENT_PARTS['os'][random.choice(USER_AGENT_PARTS['os'].keys())]
        os_name = random.choice(os['name']) 
        sysinfo = os_name

        # Choose random platform
        platform = USER_AGENT_PARTS['platform'][
                    random.choice(USER_AGENT_PARTS['platform'].keys())]

        # Get Browser Information if available
        if 'browser_info' in platform and platform['browser_info']:
            browser = platform['browser_info']
            browser_string = random.choice(browser['name'])
            if 'ext_pre' in browser:
                browser_string = "%s; %s" % (random.choice(browser['ext_pre']), 
                                                           browser_string)

            sysinfo = "%s; %s" % (browser_string, sysinfo)
            if 'ext_post' in browser:
                sysinfo = "%s; %s" % (sysinfo, random.choice(browser['ext_post']))

        if 'ext' in os and os['ext']:
            sysinfo = "%s; %s" % (sysinfo, random.choice(os['ext']))

        ua_string = "%s (%s)" % (mozilla_version, sysinfo)

        if 'name' in platform and platform['name']:
            ua_string = "%s %s" % (ua_string, random.choice(platform['name']))

        if 'details' in platform and platform['details']:
            ua_string = "%s (%s)" % (ua_string, random.choice(platform['details']) 
                                    if len(platform['details']) > 1 
                                    else platform['details'][0])

        if 'extensions' in platform and platform['extensions']:
            ua_string = "%s %s" % (ua_string, 
                                   random.choice(platform['extensions']))

        return ua_string


    def generateRandomHeaders(self):
        # Random no-cache entries
        noCacheDirectives = ['no-cache', 'max-age=0']
        random.shuffle(noCacheDirectives)
        nrNoCache = random.randint(1, (len(noCacheDirectives)-1))
        noCache = ', '.join(noCacheDirectives[:nrNoCache])

        # Random accept encoding
        acceptEncoding = ['\'\'','*','identity','gzip','deflate']
        random.shuffle(acceptEncoding)
        nrEncodings = random.randint(1, len(acceptEncoding)/2)
        roundEncodings = acceptEncoding[:nrEncodings]

        http_headers = {
            'User-Agent': self.getUserAgent(),
            'Cache-Control': noCache,
            'Accept-Encoding': ', '.join(roundEncodings),
            'Connection': 'keep-alive',
            'Keep-Alive': str(random.randint(1,1000)),
    #        'Host': self.host,
        }

        # Randomly-added headers
        # These headers are optional and are 
        # randomly sent thus making the
        # header count random and unfingerprintable
        if random.randrange(2) == 0:
            # Random accept-charset
            acceptCharset = ['ISO-8859-1', 'utf-8', 'Windows-1251', 
                             'ISO-8859-2', 'ISO-8859-15',]
            random.shuffle(acceptCharset)
            http_headers['Accept-Charset'] = '{0},{1};q={2},*;q={3}'.format(
                    acceptCharset[0], 
                    acceptCharset[1],round(random.random(), 1), 
                    round(random.random(), 1))

#        if random.randrange(2) == 0:
#            # Random Referer
#            url_part = self.buildblock(random.randint(5,10))
#
#            random_referer = random.choice(self.referers) + url_part
#
#            if random.randrange(2) == 0:
#                random_referer = random_referer + '?' + \
#                                 self.generateQueryString(random.randint(1, 10))
#
#            http_headers['Referer'] = random_referer

        if random.randrange(2) == 0:
            # Random Content-Type
            http_headers['Content-Type'] = random.choice(['multipart/form-data', 
                                            'application/x-url-encoded'])

        if random.randrange(2) == 0:
            # Random Cookie
            http_headers['Cookie'] = self.generateQueryString(
                    random.randint(1, 5))

        # random time pause between requests
        time.sleep(random.randint(3, 7))

        return http_headers
