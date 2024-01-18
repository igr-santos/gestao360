create or replace view public.view_split_songs as
	select
		sq.distributionreport_id,
		sq.stakeholder_id,
		UPPER(cs.title) as title,
		sum(sq.amount) as amount,
		round(sum(sq.exchange_amount)::numeric, 2) as exchange_amount,
		sq.split,
		sum(sq.income) as income,
		round(sum(sq.exchange_income)::numeric, 2) as exchange_income
	from (
		select
			dr.id as distributionreport_id,
			sh.id as stakeholder_id,
			split.song_id as song_id,
			ss.album,
			ss.title,
			sp.amount as amount,
			(sp.amount * (dr.income / dr.amount)) as exchange_amount,
			sl.value as split,
			(sp.amount * (sl.value / 100)) as income,
			((sp.amount * (sl.value / 100)) * (dr.income / dr.amount)) as exchange_income
		from split_splitreportpayment sp
		inner join split_splitsong ss on ss.id = sp.split_song_id
		inner join split_split split on split.id = ss.split_id 
		inner join split_splitline sl on sl.split_id = ss.split_id
		inner join stakeholders_stakeholder sh on sh.id = sl.owner_id
		inner join reports_distributionreport dr on dr.id = sp.report_id
	) as sq
	inner join copyright_song cs on cs.id = sq.song_id
	group by sq.distributionreport_id, sq.stakeholder_id, cs.title, sq.split
;
