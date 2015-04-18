AR = 'C:\\Anaconda\\Scripts\\ar.bat'
ARFLAGS = 'rcs'
CC = ['C:\\Anaconda\\Scripts\\gcc.bat']
CCDEFINES = ['WIN32', 'LAUNCH_DEBUG', 'NDEBUG', 'WINDOWED']
CCDEFINES_ST = '-D%s'
CCFLAGS = ['-Wdeclaration-after-statement', '-Werror', '-mms-bitfields', '-m32']
CCFLAGS_DEBUG = ['-g']
CCFLAGS_MACBUNDLE = ['-fPIC']
CCFLAGS_RELEASE = ['-O2']
CCLNK_SRC_F = ''
CCLNK_TGT_F = ['-o', '']
CC_NAME = 'gcc'
CC_SRC_F = ''
CC_TGT_F = ['-c', '-o', '']
CC_VERSION = ('4', '7', '0')
CPP = 'C:\\Anaconda\\Scripts\\cpp.bat'
CPPPATH = ['../zlib', '..\\common']
CPPPATH_ST = '-I%s'
DEST_CPU = 'x86'
DEST_OS = 'win32'
FULLSTATIC_MARKER = '-static'
IMPLIB_ST = '-Wl,--out-implib,%s'
LIBPATH_ST = '-L%s'
LIB_COMCTL32 = ['comctl32']
LIB_KERNEL32 = ['kernel32']
LIB_ST = '-l%s'
LIB_USER32 = ['user32']
LIB_WS2_32 = ['ws2_32']
LINKFLAGS = ['-Wl,--enable-auto-import', '-mwindows']
LINKFLAGS_MACBUNDLE = ['-bundle', '-undefined', 'dynamic_lookup']
LINK_CC = ['C:\\Anaconda\\Scripts\\gcc.bat']
MYARCH = '32bit'
MYMACHINE = None
NAME = 'default'
PREFIX = 'C:\\users\\nico_000\\appdata\\local\\temp'
RANLIB = 'C:\\Anaconda\\Scripts\\ranlib.bat'
RPATH_ST = '-Wl,-rpath,%s'
SHLIB_MARKER = '-Wl,-Bdynamic'
SONAME_ST = '-Wl,-h,%s'
STATICLIBPATH_ST = '-L%s'
STATICLIB_MARKER = '-Wl,-Bstatic'
STATICLIB_ST = '-l%s'
WINRC = 'C:\\Anaconda\\Scripts\\windres.bat'
WINRCFLAGS = ''
WINRC_SRC_F = '-i'
WINRC_TGT_F = '-o'
_VARIANT_ = 'debugw'
implib_PATTERN = 'lib%s.dll.a'
macbundle_PATTERN = '%s.bundle'
program_PATTERN = '%s.exe'
shlib_CCFLAGS = ['-DPIC', '-DDLL_EXPORT']
shlib_LINKFLAGS = ['-shared']
shlib_PATTERN = '%s.dll'
staticlib_LINKFLAGS = ['-Wl,-Bstatic']
staticlib_PATTERN = 'lib%s.a'
