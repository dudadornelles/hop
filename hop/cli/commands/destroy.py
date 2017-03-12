from hop.cli.commands import get_provider


def execute(args, **kwargs):  # pylint: disable=unused-argument
    hop_config = kwargs['hop_config']

    if not args.force:
        print("\n-- WARNING: this will destroy permanently resources:")
        print("      * server named '{}'".format(hop_config.server_name))
        print("      * agents with prefix '{}'\n".format(hop_config.agents_prefix))

        should_continue = input("\n Are you sure you want to continue? (y/n) : ")
        if should_continue.startswith('n'):
            exit(0)

    get_provider(hop_config).destroy(args, hop_config)
