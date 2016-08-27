#!/usr/bin/env python
import click
import pyparsing
import os
import colorama
import subprocess

from noxscript.decompiler import Decompiler

# increase the recursion limit
import sys
sys.setrecursionlimit(5000)

@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('scrobj', type=click.File('rb'))
@click.option('--out', '-o', default=None, help='Output file path.')
@click.option('--analyze/--no-analyze', default=True, help='Perform structural analysis.')
@click.option('--pprint/--no-pprint', default=True, help='Run astyle on output.')
@click.option('--verbose', '-v', is_flag=True, help='Verbose mode. Prints AST.')
def cli(scrobj, out, analyze, pprint, verbose):
    '''
    NoxScript 3.0 Decompiler - By Andrew Wesie (zoaedk) and Brian Pak (cai)
    '''
    try:
        try:
            d = Decompiler(scrobj, struct_analysis=analyze)
        except Exception as e:
            click.secho('Error: %s' % e, fg='red')
            return

        if out is None:
            out = './%s.ns' % (os.path.splitext(os.path.basename(scrobj.name))[0])

        if verbose:
            d.print_ast()
        d.unparse(out)

        if pprint:
            subprocess.check_call(['astyle', '--mode=c', '--style=break', '-Y', '-j', '-q', '-n', out])
    except Exception as e:
        click.secho('Error: %s' % e, fg='red')

if __name__ == '__main__':
    cli()
