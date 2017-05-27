for pkg in `find src -maxdepth 2 -name setup.py -printf '%h\n'`; do
    ~/bin/pip install -qe $pkg
done

# Unknwon argument, assume that user wants to run his own process,
# for example a `bash` shell to explore this image
exec "$@"
