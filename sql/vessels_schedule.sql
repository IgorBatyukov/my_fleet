-- public.vessels_schedule source

CREATE MATERIALIZED VIEW public.vessels_schedule
TABLESPACE pg_default
AS WITH schedule AS (
         SELECT ov.id,
            ov.vessel_id,
            gs.name AS departure_port,
            gs2.name AS destination_port,
            od2.eta,
            oa.name AS agency
           FROM operations_voyage ov
             JOIN operations_departureport od ON ov.id = od.voyage_id
             JOIN geo_seaport gs ON od.seaport_id = gs.id
             JOIN operations_destinationport od2 ON ov.id = od2.voyage_id
             LEFT JOIN operations_agency oa ON oa.id = od2.agency_id
             JOIN geo_seaport gs2 ON od2.seaport_id = gs2.id
          WHERE od2.arrival_date_time IS NULL
        ), positions AS (
         SELECT ov2.voyage_num,
            ov2.type,
            fv_1.id,
            ov.operation,
            max(ov.report_date_time) AS report_date
           FROM operations_vesselpositionreport ov
             JOIN fleet_vessel fv_1 ON fv_1.id = ov.vessel_id
             JOIN operations_voyage ov2 ON ov2.id = ov.voyage_id
          GROUP BY ov2.voyage_num, ov2.type, fv_1.id, ov.operation
        )
 SELECT s.id,
    fv.id AS vessel_id,
    fv.name AS vessel_name,
    ff.name AS fleet,
    s.departure_port,
    s.destination_port,
    s.eta,
    s.agency,
    p.type,
    p.voyage_num,
    p.operation,
    p.report_date
   FROM fleet_vessel fv
     JOIN fleet_fleet ff ON ff.id = fv.fleet_id
     LEFT JOIN schedule s ON s.vessel_id = fv.id
     LEFT JOIN positions p ON p.id = fv.id
WITH DATA;