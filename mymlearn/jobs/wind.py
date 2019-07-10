# coding:utf8
from WindPy import w
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from utils.mymysql import MyMySQL


class WindAPI:
    '''
    windAPI获取三大报表数据
    '''
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://spider:SzPj24^365wx@39.97.184.89:3306/spider?charset=utf8')
        self.count = 0 # API计数 每周限额50W个单元格
        self.three_report_fields =  {
            'balance':"monetary_cap,tradable_fin_assets,acctandnotes_rcv,notes_rcv,acct_rcv,prepay,oth_rcv_tot,dvd_rcv,int_rcv,oth_rcv,inventories,consumptive_bio_assets,cont_assets,deferred_exp,hfs_assets,non_cur_assets_due_within_1y,settle_rsrv,loans_to_oth_banks,margin_acct,prem_rcv,rcv_from_reinsurer,rcv_from_ceded_insur_cont_rsrv,red_monetary_cap_for_sale,tot_acct_rcv,oth_cur_assets,cur_assets_gap,cur_assets_gap_detail,cur_assets_netting,tot_cur_assets,fin_assets_chg_compreh_inc,fin_assets_amortizedcost,debt_invest,oth_debt_invest,fin_assets_avail_for_sale,oth_eqy_instruments_invest,held_to_mty_invest,oth_non_cur_fina_asset,invest_real_estate,long_term_eqy_invest,long_term_rec,fix_assets_tot,fix_assets,fix_assets_disp,const_in_prog_tot,const_in_prog,proj_matl,productive_bio_assets,oil_and_natural_gas_assets,intang_assets,r_and_d_costs,goodwill,long_term_deferred_exp,deferred_tax_assets,loans_and_adv_granted,oth_non_cur_assets,non_cur_assets_gap,non_cur_assets_gap_detail,non_cur_assets_netting,tot_non_cur_assets,cash_deposits_central_bank,agency_bus_assets,rcv_invest,asset_dep_oth_banks_fin_inst,precious_metals,rcv_ceded_unearned_prem_rsrv,rcv_ceded_claim_rsrv,rcv_ceded_life_insur_rsrv,rcv_ceded_lt_health_insur_rsrv,insured_pledge_loan,cap_mrgn_paid,independent_acct_assets,time_deposits,subr_rec,mrgn_paid,seat_fees_exchange,clients_cap_deposit,clients_rsrv_settle,oth_assets,derivative_fin_assets,assets_gap,assets_gap_detail,assets_netting,tot_assets,st_borrow,tradable_fin_liab,acctandnotes_payable,notes_payable,acct_payable,adv_from_cust,cont_liab,empl_ben_payable,taxes_surcharges_payable,tot_acct_payable,oth_payable_tot,int_payable,dvd_payable,oth_payable,acc_exp,deferred_inc_cur_liab,hfs_liab,non_cur_liab_due_within_1y,st_bonds_payable,borrow_central_bank,deposit_received_ib_deposits,loans_oth_banks,fund_sales_fin_assets_rp,handling_charges_comm_payable,payable_to_reinsurer,rsrv_insur_cont,acting_trading_sec,acting_uw_sec,oth_cur_liab,cur_liab_gap,cur_liab_gap_detail,cur_liab_netting,tot_cur_liab,lt_borrow,bonds_payable,lt_payable_tot,lt_payable,lt_empl_ben_payable,specific_item_payable,provisions,deferred_tax_liab,deferred_inc_non_cur_liab,oth_non_cur_liab,non_cur_liab_gap,non_cur_liab_gap_detail,non_cur_liab_netting,tot_non_cur_liab,liab_dep_oth_banks_fin_inst,agency_bus_liab,cust_bank_dep,claims_payable,dvd_payable_insured,deposit_received,insured_deposit_invest,unearned_prem_rsrv,out_loss_rsrv,life_insur_rsrv,lt_health_insur_v,independent_acct_liab,prem_received_adv,pledge_loan,st_finl_inst_payable,oth_liab,derivative_fin_liab,liab_gap,liab_gap_detail,liab_netting,tot_liab,cap_stk,other_equity_instruments,other_equity_instruments_PRE,perpetual_debt,cap_rsrv,surplus_rsrv,undistributed_profit,tsy_stk,other_compreh_inc_bs,special_rsrv,prov_nom_risks,cnvd_diff_foreign_curr_stat,unconfirmed_invest_loss_bs,shrhldr_eqy_gap,shrhldr_eqy_gap_detail,shrhldr_eqy_netting,eqy_belongto_parcomsh,minority_int,tot_equity,liab_shrhldr_eqy_gap,liab_shrhldr_eqy_gap_detail,liab_shrhldr_eqy_netting,tot_liab_shrhldr_eqy",
            'profit':"tot_oper_rev,oper_rev,int_inc,insur_prem_unearned,handling_chrg_comm_inc,tot_prem_inc,reinsur_inc,prem_ceded,unearned_prem_rsrv_withdraw,net_inc_agencybusiness,net_inc_underwriting-business,net_inc_customerasset-managementbusiness,other_oper_inc,net_int_inc,net_fee_and_commission_inc,net_other_oper_inc,tot_oper_cost,oper_cost,int_exp,handling_chrg_comm_exp,oper_exp,taxes_surcharges_ops,selling_dist_exp,gerl_admin_exp,rd_exp,fin_exp_is,fin_int_exp,fin_int_inc,impair_loss_assets,credit_impair_loss,prepay_surr,net_claim_exp,net_insur_cont_rsrv,dvd_exp_insured,reinsurance_exp,claim_exp_recoverable,Insur_rsrv_recoverable,reinsur_exp_recoverable,other_oper_exp,net_inc_other_ops,net_gain_chg_fv,net_invest_inc,inc_invest_assoc_jv_entp,net_exposure_hedge_ben,net_gain_fx_trans,gain_asset_dispositions,other_grants_inc,opprofit_gap,opprofit_gap_detail,opprofit_netting,opprofit,non_oper_rev,non_oper_exp,net_loss_disp_noncur_asset,profit_gap,profit_gap_detail,profit_netting,tot_profit,tax,unconfirmed_invest_loss_is,net_profit_is_gap,net_profit_is_gap_detail,net_profit_is_netting,net_profit_is,net_profit_continued,net_profit_discontinued,minority_int_inc,np_belongto_parcomsh,eps_basic_is,eps_diluted_is,other_compreh_inc,tot_compreh_inc,tot_compreh_inc_min_shrhldr,tot_compreh_inc_parent_comp",
            'cashflow':"cash_recp_sg_and_rs,recp_tax_rends,other_cash_recp_ral_oper_act,net_incr_insured_dep,net_incr_dep_cob,net_incr_loans_central_bank,net_incr_fund_borr_ofi,net_incr_int_handling_chrg,cash_recp_prem_orig_inco,net_cash_received_reinsu_bus,net_incr_disp_tfa,net_incr_disp_fin_assets_avail,net_incr_loans_other_bank,net_incr_repurch_bus_fund,net_cash_from_seurities,cash_inflows_oper_act_gap,cash_inflows_oper_act_gap_detail,cash_inflows_oper_act_netting,stot_cash_inflows_oper_act,net_incr_lending_fund,net_fina_instruments_measured_at_fmv,cash_pay_goods_purch_serv_rec,cash_pay_beh_empl,pay_all_typ_tax,other_cash_pay_ral_oper_act,net_incr_clients_loan_adv,net_incr_dep_cbob,cash_pay_claims_orig_inco,handling_chrg_paid,comm_insur_plcy_paid,cash_outflows_oper_act_gap,cash_outflows_oper_act_gap_detail,cash_outflows_oper_act_netting,stot_cash_outflows_oper_act,cf_oper_act_netting,net_cash_flows_oper_act,cash_recp_disp_withdrwl_invest,cash_recp_return_invest,net_cash_recp_disp_fiolta,net_cash_recp_disp_sobu,other_cash_recp_ral_inv_act,cash_inflows_inv_act_gap,cash_inflows_inv_act_gap_detail,cash_inflows_inv_act_netting,stot_cash_inflows_inv_act,cash_pay_acq_const_fiolta,cash_paid_invest,net_incr_pledge_loan,net_cash_pay_aquis_sobu,other_cash_pay_ral_inv_act,cash_outflows_inv_act_gap,cash_outflows_inv_act_gap_detail,cash_outflows_inv_act_netting,stot_cash_outflows_inv_act,cf_inv_act_netting,net_cash_flows_inv_act,cash_recp_cap_contrib,cash_rec_saims,cash_recp_borrow,other_cash_recp_ral_fnc_act,proc_issue_bonds,cash_inflows_fnc_act_gap,cash_inflows_fnc_act_gap_detail,cash_inflows_fnc_act_netting,stot_cash_inflows_fnc_act,cash_prepay_amt_borr,cash_pay_dist_dpcp_int_exp,dvd_profit_paid_sc_ms,other_cash_pay_ral_fnc_act,cash_outflows_fnc_act_gap,cash_outflows_fnc_act_gap_detail,cash_outflows_fnc_act_netting,stot_cash_outflows_fnc_act,cf_fnc_act_netting,net_cash_flows_fnc_act,eff_fx_flu_cash,net_incr_cash_cash_equ_gap,net_incr_cash_cash_equ_gap_detail,net_incr_cash_cash_equ_netting,net_incr_cash_cash_equ_dm,cash_cash_equ_beg_period,cash_cash_equ_end_period,net_profit_cs,prov_depr_assets,depr_fa_coga_dpba,amort_intang_assets,amort_lt_deferred_exp,decr_deferred_exp,incr_acc_exp,loss_disp_fiolta,loss_scr_fa,loss_fv_chg,fin_exp_cs,invest_loss,decr_deferred_inc_tax_assets,incr_deferred_inc_tax_liab,decr_inventories,decr_oper_payable,incr_oper_payable,unconfirmed_invest_loss_cs,others,im_net_cash_flows_oper_act_gap,im_net_cash_flows_oper_act_gap_detail,im_net_cash_flows_oper_act_netting,im_net_cash_flows_oper_act,conv_debt_into_cap,conv_corp_bonds_due_within_1y,fa_fnc_leases,end_bal_cash,beg_bal_cash,end_bal_cash_equ,beg_bal_cash_equ,im_net_incr_cash_cash_equ_gap,im_net_incr_cash_cash_equ_gap_detail,im_net_incr_cash_cash_equ_netting,net_incr_cash_cash_equ_im",
        }

    def __enter__(self):
        w.start()
        return self

    def getStocks(self,n):
        df = pd.read_sql_query(f"select stock_code from spider.com_status where id>{200*n} and id<{200*n+200}",self.engine)
        return df.stock_code.values.tolist()

    def mytest(self,stock_code,fields,periodDate):
        data = w.wss(stock_code,fields,f"unit=1;rptDate={periodDate};rptType=1")
        print(data)

    def run(self):
        for n in range(7):
            stocks = self.getStocks(n)
            for k,v in self.three_report_fields.items():
                data = w.wss(stocks, v, "unit=1;rptDate=20181231;rptType=1")
                dfc = pd.DataFrame()
                for i,column in enumerate(data.Fields):
                    dfc[column] = data.Data[i]
                dfc["stock_code"] = stocks
                print(dfc.shape)
                dfc.to_sql(k,self.engine,index=False)
                with MyMySQL() as m:
                    m.execute_sql("create table if not exists com_{0} like {0}".format(k))
                    m.execute_sql("insert into com_{0} select * from {0}".format(k))
                    m.execute_sql("drop table {0}".format(k))

    def __exit__(self, exc_type, exc_val, exc_tb):
        w.close()


if __name__=="__main__":
    with WindAPI() as wp:
        wp.mytest("600000.SH","eps_ttm","20181230")