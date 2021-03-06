from distutils.core import setup
from distutils.command.install_scripts import install_scripts

class post_install(install_scripts):

    def run(self):
        install_scripts.run(self)

        from shutil import move
        for i in self.get_outputs():
            n = i.replace('.py', '')
            move(i, n)
            print "moving '{0}' to '{1}'".format(i, n)


ID = 'org.sbillaudelle.KeyboardManager'
data_files = [
    ('share/cream/{0}/configuration'.format(ID),
        ['src/configuration/scheme.xml']),
    ('share/cream/{0}/'.format(ID),
        ['src/manifest.xml']),
    ('share/cream/{0}/data'.format(ID),
        ['src/data/keyboard.png'])
    ]


setup(
    name = 'keyboard-manager',
    version = '0.1',
    author = 'Sebastian Billaudelle',
    url = 'http://github.com/sbillaudelle/keyboard-manager',
    data_files = data_files,
    cmdclass={'install_scripts': post_install},
    scripts = ['src/keyboard-manager.py']
)
