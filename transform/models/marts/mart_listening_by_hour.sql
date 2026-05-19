with base as (
    select * from {{ ref('stg_played_tracks') }}
)

select
    played_hour,
    count(*)                        as total_plays,
    round(sum(duration_minutes), 2) as total_minutes_listened
from base
group by played_hour
order by played_hour