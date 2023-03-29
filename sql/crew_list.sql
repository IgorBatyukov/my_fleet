-- public.crew_list source

CREATE MATERIALIZED VIEW public.crew_list
TABLESPACE pg_default
AS WITH last_contract AS (
         WITH ranked_contract AS (
                 SELECT cc_1.crew_id,
                    cc_1.vessel_id,
                    cc_1.signed_date,
                    rank() OVER (PARTITION BY cc_1.crew_id ORDER BY cc_1.signed_date DESC) AS rank
                   FROM crew_contract cc_1
                )
         SELECT ranked_contract.crew_id,
            ranked_contract.vessel_id,
            ranked_contract.signed_date,
            ranked_contract.rank
           FROM ranked_contract
          WHERE ranked_contract.rank = 1
        )
 SELECT cc.id,
    concat(cc.name, ' ', cc.father_name, ' ', cc.surname) AS crew_name,
    cr.id AS rank_id,
    cr.name AS rank,
        CASE
            WHEN cc.working_status::text = 'at_home'::text THEN 'Sailor is on vacation'::text
            WHEN cc.working_status::text = 'at_sea'::text THEN 'Sailor is at sea'::text
            ELSE NULL::text
        END AS working_status,
    fv.name AS vessel_name,
    cc.fleet_id,
    lc.signed_date
   FROM crew_crewmember cc
     JOIN crew_rank cr ON cr.id = cc.rank_id
     LEFT JOIN last_contract lc ON lc.crew_id = cc.id
     LEFT JOIN fleet_vessel fv ON fv.id = lc.vessel_id
  ORDER BY cr.id
WITH DATA;

-- View indexes:
CREATE UNIQUE INDEX idx_crew_id ON public.crew_list USING btree (id);