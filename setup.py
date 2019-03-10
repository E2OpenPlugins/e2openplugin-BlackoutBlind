from distutils.core import setup
import setup_translate

pkg = 'Extensions.BlackoutBlind'
setup (name = 'enigma2-plugin-extensions-blackoutblind',
       version = '1.3.0',
       description = 'hide white dotted (VBI) lines on top of the screen',
       packages = [pkg],
       package_dir = {pkg: 'plugin'},
       package_data = {pkg: ['*.png', 'locale/*/LC_MESSAGES/*.mo']},
       cmdclass = setup_translate.cmdclass, # for translation
      )
