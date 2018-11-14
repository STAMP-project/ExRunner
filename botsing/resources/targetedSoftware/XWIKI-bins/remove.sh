DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

find $(pwd) -maxdepth 20 -type f -name '*-version.jar' | while read candidates; do
  rm $candidates
  echo "$candidates Removed!"
done
