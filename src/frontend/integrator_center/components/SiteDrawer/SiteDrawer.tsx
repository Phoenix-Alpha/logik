import {
  BarChartOutlined,
  FolderFilled,
  SettingOutlined,
} from "@ant-design/icons";
import { Avatar, Collapse, Drawer, Menu } from "antd";
import { FC, memo } from "react";
import styled from "styled-components";

const StyledDrawerAvatar = styled(Avatar)`
  margin: 0 16px;
`;

const StyledDrawerProfileHeader = styled.div`
  display: flex;
  flex-direction: column;
`;

export interface ISiteDrawerProps {
  title?: string;
  visible: boolean;
  closeDrawer?: () => void;
}

export const SiteDrawer: FC<ISiteDrawerProps> = memo(
  ({ title, visible, closeDrawer }: ISiteDrawerProps) => {
    const onClose = () => {
      if (closeDrawer) {
        closeDrawer();
      }
    };

    return (
      <Drawer
        title={title}
        placement="left"
        onClose={onClose}
        visible={visible}
        width="280"
        closable={false}
        bodyStyle={{ padding: "20px 0" }}
      >
        <StyledDrawerAvatar>SB</StyledDrawerAvatar>
        <Collapse bordered={false} expandIconPosition="right">
          <Collapse.Panel
            key="1"
            header={[
              <StyledDrawerProfileHeader key="drawer-profile-header-key">
                <div>Simon Bonnacié</div>
                <div>Simon Bonnacié@klocel.com</div>
              </StyledDrawerProfileHeader>,
            ]}
          >
            <div>Simon Bonnacié</div>
            <div>Simon Bonnacié@klocel.com</div>
          </Collapse.Panel>
        </Collapse>
        <Menu defaultSelectedKeys={["1"]} mode="inline">
          <Menu.SubMenu
            key="general-settings"
            icon={<SettingOutlined />}
            title="General Settings"
          >
            <Menu.Item key="general-settings-profile">Profile</Menu.Item>
            <Menu.Item key="general-settings-spaces">Spaces</Menu.Item>
            <Menu.Item key="general-settings-users">Users</Menu.Item>
            <Menu.Item key="general-settings-customer">Customer</Menu.Item>
          </Menu.SubMenu>
          <Menu.SubMenu
            key="development-center"
            icon={<SettingOutlined />}
            title="Development Center"
          >
            <Menu.Item key="development-center-store">Store</Menu.Item>
            <Menu.Item key="development-center-ui-manager">
              UI Manager
            </Menu.Item>
            <Menu.Item key="development-center-dictionary-manager">
              Dictionary Manager
            </Menu.Item>
            <Menu.Item key="development-center-document-manager">
              Document Manager
            </Menu.Item>
            <Menu.Item key="development-center-flow-manager">
              Flow Manager
            </Menu.Item>
            <Menu.Item key="development-center-bi-manager">
              BI Manager
            </Menu.Item>
            <Menu.Item key="development-center-widgets-manager">
              Widgets Manager
            </Menu.Item>
          </Menu.SubMenu>
          <Menu.SubMenu
            key="billing"
            icon={<BarChartOutlined />}
            title="Billing"
          >
            <Menu.Item key="billing-statistics">Statistics</Menu.Item>
            <Menu.Item key="billing-invoices">Invoices</Menu.Item>
          </Menu.SubMenu>
          <Menu.SubMenu
            key="documentation"
            icon={<FolderFilled />}
            title="Documentation"
          >
            <Menu.Item key="documentation-functional">Functional</Menu.Item>
            <Menu.Item key="documentation-technical">Technical</Menu.Item>
          </Menu.SubMenu>
        </Menu>
      </Drawer>
    );
  }
);

SiteDrawer.displayName = "SiteDrawer";

export default SiteDrawer;
