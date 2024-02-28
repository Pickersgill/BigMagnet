import os, sys, argparse, tarfile, re

class Unpacker:
    def __init__(self):
        pass

    def unpack(self, archive_dir, archive_name, pattern, dest, delete=False):
        src_path = os.path.join(archive_dir, archive_name)
        dest_path = os.path.join(dest, archive_name+".dump")
    
        print(f"Unpacking {src_path}...")
        tar = tarfile.open(src_path, "r:gz")
        members = list(filter(lambda x : re.match(pattern, x.name), tar.getmembers()))
        tar.extractall(dest_path, members=members)
        with open(os.path.join(dest_path, "meta"), "w+") as meta:
            names = "\n".join([m.name for m in members]) + "\n"
            meta.write(names)
    
        if delete:
            os.remove(src_path)
        
        return len(members)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # TODO implement -f flattion argument to flatten output directories
    
    parser.add_argument("-s", "--src-directory", help="directory containing archives", type=str, required=True)
    parser.add_argument("-d", "--delete", help="toggles deletion of archives once extracted", action="store_true", default=False)
    parser.add_argument("-o", "--output-directory", help="directory to place extracted files", type=str, required=False, default=None)
    parser.add_argument("-r", "--replace", help="archives will be deleted and replaced with extracted contents, equivalent to -s <dir> -o <dir> -d", default=False, action="store_true") 
    parser.add_argument("-q", "--query", help="valid python regular expression used to determine if file should be kept", required=True, type=str)
    parser.add_argument("-c", "--create", help="toggle creation of output dir if doesn't exist", default=False, action="store_true")

    args = parser.parse_args()

    if not args.output_directory:
        args.output_directory = args.src_directory

    if args.replace:
        args.delete = True
        args.output_directory = args.src_directory
    
    if not os.path.exists(args.output_directory):
        if not args.create:
            parser.error(f"Output path {args.output_directory} does not exist. Use -c to force creation of missing output directory")
        else:
            os.mkdir(args.output_directory)
    
    up = Unpacker()
    
    archives = os.listdir(args.src_directory)
    total = 0
    for archive in archives:
        total += up.unpack(args.src_directory, archive, args.query, args.output_directory, args.delete)

    print(f"Extraction complete. Found {total} files matching your query")
    
        
