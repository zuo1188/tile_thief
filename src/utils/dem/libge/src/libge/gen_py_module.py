import os
import sys
from pygccxml import parser
from pyplusplus import module_builder

generator_path="C:/soft/gccxml-master/build/bin/Debug/gccxml.exe"
generator_name="gccxml"
compiler="cl"
compiler_path="C:/Program\ Files\ (x86)/Microsoft\ Visual\ Studio\ 12.0/VC/bin/cl.exe"

xml_generator_config=parser.xml_generator_configuration_t(xml_generator_path=generator_path,
                                                   xml_generator=generator_name,
                                                    compiler=compiler,
                                                   compiler_path=compiler_path)

header_collection=["libge.h"]

builder=module_builder.module_builder_t(header_collection,xml_generator_path=generator_path,
                                        xml_generator_config=xml_generator_config)


# mb = module_builder.module_builder_t(files=['libge.h'], gccxml_path='/', generator_name="gccxml")

builder.build_code_creator( module_name='libge_py' ) #要生成的python模块的名称

builder.code_creator.user_defined_directories.append( os.path.abspath('.') )

builder.write_module( os.path.join( os.path.abspath('.'), 'libge_py.cc' ) )