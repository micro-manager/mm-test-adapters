# replace the version by running:
# meson rewrite kwargs set project / version $(python scripts/extract_version.py)
project(
  'mmcore-test-devices',
  'cpp',
  version : '11.5.0.73.0',
  meson_version : '>= 1.2.0',
  default_options : ['cpp_std=c++14']
)

subdir('src/mmCoreAndDevices/MMDevice')
subdir('src/mmCoreAndDevices/MMCore')
subdir('src/mmCoreAndDevices/DeviceAdapters')

mmdevice_dep = dependency('mmdevice_dep')
mmcore_dep   = dependency('mmcore_dep')

cpp_args = ['-DMMDEVICE_CLIENT_BUILD']
if host_machine.system() == 'windows'
    cpp_args += ['-DNOMINMAX', '-D_CRT_SECURE_NO_WARNINGS']
endif
