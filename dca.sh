#!/bin/sh

cd "$(dirname "$0")"

ENVIRONMENT="$1"
EKEY="$2"
MAIL_ADDR="$3"
#FROM_ADDR="$4"
COMMAND="$4"
EXEC_TIME="$(date '+%F-%H.%M.%S')"
LOG_DIR="$(dirname $0)/logs"
LOG_FILE="${LOG_DIR}/weekly-dca-${EXEC_TIME}.log"

showUsageAndDie()
{
  echo "Usage:"
  #echo "$(basename $0) environment ekey toEmail fromEmail command"
  echo "$(basename $0) environment ekey email command"
  exit 1
}

if [ -z "${ENVIRONMENT}" ]
then
  echo "ERROR:  No environment specified."
  showUsageAndDie
fi

if [ -z "${EKEY}" ]
then
  echo "ERROR:  No ekey provided."
  showUsageAndDie
fi

if [ -z "${MAIL_ADDR}" ]
then
  echo "ERROR:  No email provided."
  showUsageAndDie
fi

# Run the program.
. "${ENVIRONMENT}"
if [ -z "${COMMAND}" ]
then
  python cb-adv-dca.py "${EKEY}" >> "${LOG_FILE}" 2>&1
else
  # The COMMAND argument is not quoted so that it can expand.
  python cb-adv-dca.py ${COMMAND} "${EKEY}" >> "${LOG_FILE}" 2>&1
fi

# Send the output when complete.
#mail -f "${FROM_ADDR}" -s "CBP weekly DCA for ${EXEC_TIME}" "${MAIL_ADDR}" < "${LOG_FILE}"
mail -s "CBP weekly DCA for ${EXEC_TIME}" "${MAIL_ADDR}" < "${LOG_FILE}"
