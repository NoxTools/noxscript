#!/usr/bin/env python
import click
import pyparsing
import os
import colorama

from noxscript.compiler import Compiler

@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('source', type=click.File('rb'))
@click.option('--out', '-o', default=None, help='Output file path.')
@click.option('--verbose', '-v', is_flag=True, help='Verbose mode. Displays script information.')
def cli(source, out, verbose):
    '''
    NoxScript 3.0 Compiler - By Andrew Wesie (zoaedk) and Brian Pak (cai)
    '''
    try:
        try:
            c = Compiler(source.read())
        except pyparsing.ParseException:
            click.secho('Error: Parse error. Check your source again.', fg='red')
            return
        except Exception as e:
            click.secho('Error: %s' % e, fg='red')
            return

        if out is None:
            out = './%s.obj' % (os.path.splitext(os.path.basename(source.name))[0])

        with open(out, 'wb') as fp:
            info = c.compile(fp)
        click.echo('Compiled ' + click.style('%s' % source.name, fg='yellow') +
                ': ' + click.style('%s' % out, fg='green') +
                ' (' + click.style('%d bytes' % info['size'], fg='cyan') +')')
        if verbose:
            strings = info['strings'][1:]
            funcs = info['funcs']
            click.secho('\nScript Info:', bold=True)
            click.echo('[+] ' + click.style('%d' % len(strings), fg='cyan') + ' strings')
            click.echo('  0: <NOT_USED>')
            for s, i in strings:
                click.echo('%3d: %s' % (i, s))
            click.echo('\n[+] ' + click.style('%d' % len(funcs), fg='cyan') + ' functions')
            for func in funcs:
                click.echo('%3d: %s' % (func.num, func.name))
    except Exception as e:
        click.secho('Error: %s' % e, fg='red')

if __name__ == '__main__':
    cli()
