-- public.crew_onboard source

CREATE MATERIALIZED VIEW public.crew_onboard
TABLESPACE pg_default
AS WITH valid_contract AS (
         SELECT cc_1.crew_id,
            cr.id AS rank_id,
            cr.name AS rank,
            cc_1.vessel_id,
            cc_1.signed_date,
            cc_1."offset",
            (cc_1.signed_date + '1 mon'::interval * cc_1.duration::double precision)::date AS exp_date
           FROM crew_contract cc_1
             JOIN crew_rank cr ON cr.id = cc_1.rank_id
          WHERE cc_1.finished_date IS NULL
        ), last_change AS (
         WITH ranked_change AS (
                 SELECT cc_1.crew_id,
                    cc_1.vessel_id,
                    cc_1.date AS joined_date,
                    rank() OVER (PARTITION BY cc_1.crew_id ORDER BY cc_1.date DESC) AS rank,
                    cc_1.type
                   FROM crew_crewchange cc_1
                )
         SELECT ranked_change.crew_id,
            ranked_change.vessel_id,
            ranked_change.joined_date,
            ranked_change.rank,
            ranked_change.type
           FROM ranked_change
          WHERE ranked_change.rank = 1 AND ranked_change.type::text = 'join'::text
        )
 SELECT cc.id,
    concat(cc.name, ' ', cc.father_name, ' ', cc.surname) AS crew_name,
    vc.rank_id,
    vc.rank,
    fv.id AS vsl_id,
    fv.name AS vsl_name,
    vc.signed_date AS contract_signed,
    vc.exp_date AS contract_exp,
    vc."offset",
    lc.joined_date
   FROM crew_crewmember cc
     JOIN valid_contract vc ON vc.crew_id = cc.id
     JOIN fleet_vessel fv ON fv.id = vc.vessel_id
     JOIN last_change lc ON lc.crew_id = cc.id
  ORDER BY vc.rank_id, vc.vessel_id
WITH DATA;

-- View indexes:
CREATE UNIQUE INDEX idx_crewchange_id ON public.crew_onboard USING btree (id);