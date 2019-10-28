ARG image
FROM $image

ARG conf_dir

COPY --chown=101:101 create_db.sql "$conf_dir/"
COPY --chown=101:101 config.php "$conf_dir/"
COPY --chown=101:101 config.system.php "$conf_dir/"
COPY --chown=101:101 INSTALL_DISABLED "$conf_dir/"

RUN mkdir -p "$conf_dir/db"\
      && chown 101:101 "$conf_dir/db"
