FROM mahamatsaleh/msdjimet:1.0.0

HEALTHCHECK CMD curl -f http://localhost:50090/ || exit 1

ENV HDFS_CONF_dfs_checkpoint_dir=file:///hadoop/dfs/secondary
RUN mkdir -p /hadoop/dfs/secondary
VOLUME /hadoop/dfs/secondary

ADD run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 50090

CMD ["/run.sh"]